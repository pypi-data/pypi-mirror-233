
import os,sys
import numpy as np
from deepview.converter.plugin_api.args_processor import ArgsProcessor

def query_convert(src_type, dst_type):
    try:

        if src_type is None or dst_type is None:
            return {
                'supported_inputs': [{'ext':'h5','name':'Keras'}, {'ext':'pb','name':'Tensorflow'},{'ext':'onnx','name':'ONNX'},{'ext':'tflite','name':'Tensorflow Lite'}],
                'supported_outputs':[{'ext':'rtm','name':'Deepview RT'}]
            }

        ref = {    
        'panel-shuffle': {'type': 'string',   'choices': ['none', 'armv7', 'armv8', 'sse', 'avx2'], 'default': 'none','group':'debug'},
        'nnef-format': {'type': 'string',  'choices': ['nhwc', 'nchw'], 'default': 'nhwc', 'group':'debug'},
        'skip-optimizations': {'type': 'string',  'array':'', 'default': ['conv_mul4','concatN', 'sigmoid_expand', 'quantize_dequant_ops'], 'group':'debug'},
        'user-ops': {'type': 'string', 'array':'',  'default': None , 'group':'Extensions',
                        'help':'Enable user defined operations'},
       
        'force-quant-tensor': {'type': 'boolean','default': False, 'public':True, 'group':'debug',
                                'help':'Force the conversion to override partial quantization and use full quantization'},
        'activation-datatype':{ 'type': 'string', 'choices':['none', 'float32', 'int8', 'uint8'], 'default': 'none', 'group':'debug'},
        'transpose-conv-filter-datatype':{ 'type': 'string', 'choices':['none', 'float32', 'int8', 'uint8'], 'default': 'none', 'group':'debug'},
        
        'optimize-map':{'type': 'boolean',      'default': True, 'group':'debug'},
        'no-map':{'type': 'boolean',      'default': False, 'group':'debug'},
        'save-map': {'type': 'string',   'default': '', 'group':'debug'},
        'use-svm': {'type': 'string',   'default': '', 'group':'debug'},
        'save-layers': {'type': 'string',  'array':'',  'default': [], 'group':'debug'},
        'copy-layers': {'type': 'string', 'array':'',  'default': [], 'group':'debug'},

        'normalization':{   'type': 'string',  'choices':["none", "whitening", "signed", "unsigned"],'default':"none", 'group':'debug'}
        }

        if dst_type != 'rtm':
            return None

        if src_type=='onnx':
            ref['onnx-input-format']={ 'type': 'string', 'choices':['none', 'nchw', 'nhwc'], 'default': 'none'}   

        return ref
    except:
        return None


def convert(infile, outfile, params):
    try:
        args = ArgsProcessor()
        src_type=''
        dst_type=''
   
        if 'output-model-type' in params:
            dst_type = params['output-model-type']
        else:
            dst_type = args.get_dest_type(outfile)
        if 'input-model-type' in params:
            src_type=params['input-model-type']
        else:
            src_type=args.get_source_type(infile)

        
        ref = query_convert(src_type, dst_type)
        if ref is None:
            return {
                'success': 'no',
                'message': 'Not Valid file formats'
            }
        args.process(params,ref)
    
    except AttributeError as e:
        return {
            'success': 'no',
            'message': "ERROR:"+str(e)
        }

    try:
        tflite_ext = 'tflite'
        onnx_ext = 'onnx'
        rtm_ext = 'rtm'

        samples = [args.samples, args.crop]

        quant_channel_bool = True
        if args.quant_tensor:
            quant_channel_bool = False
        if args.quant_tensor and args.quant_channel:
            raise ValueError(
                "Please use only one of --quant-tensor and --quant-channel")


        if (args.force_quant_tensor and not args.quant_tensor and args.quant_channel):
            raise ValueError(
                "--force-quant-tensor is only valid when converting to RTM and enable --quant-tensor.")

        if (args.quant_tensor or args.quant_channel) and not args.quantize:
            if src_type==tflite_ext or src_type == onnx_ext:
                print("WARNING: Ensure that the input model is quantized "
                    "when using quant-tensor or quant-channel. Otherwise they "
                    "will have no effect.")
            else:
                raise ValueError("Ensure that the input model is quantized "
                                "when using quant-tensor or quant-channel. For non-TFLite/ONNX "
                                "models, use --quantize.")

        if src_type == tflite_ext and dst_type == rtm_ext and args.quantize:
            raise ValueError("TFLite models cannot be quantized when "
                            "converting to an RTM model. Either use a pre-quantized "
                            "TFLite file or use an H5, Saved Model, or TFHub model when "
                            "using the argument --quantize.")

        if src_type == onnx_ext and dst_type == rtm_ext and args.quantize:
            raise ValueError("ONNX models cannot be quantized currently when "
                            "they are the source model.")

        if args.quantize_format != 'none':
            if args.input_type != 'none' or args.output_type != 'none':
                print("Please use either --quantize_format or "
                    "--input_type and --output_type.")
                sys.exit()
            args.input_type = args.quantize_format
            args.output_type = args.quantize_format

        try:
            onnx_input_format=args.onnx_input_format
        except:
            onnx_input_format='none'

        if onnx_input_format != 'none' and (not infile.endswith(onnx_ext) or not
                                                outfile.endswith(rtm_ext)):
            raise ValueError("The argument --onnx_input_format is only for use when "
                            "converting from ONNX to RTM.")

        if args.input_names == '' or args.input_names is None:
            input_names = None
        else:
            input_names = args.input_names

        if args.output_names == '' or args.output_names is None:
            output_names = None
        else:
            output_names = args.output_names

        if args.model_input_type == 'int8':
            model_input_type = np.int8
        elif args.model_input_type == 'uint8':
            model_input_type = np.uint8
        else:
            model_input_type = np.float32

        # ----------------------------  Optimizer   -----------------------------------

        
        if args.use_svm == '':
            svm = None
        else:
            svm = args.use_svm
            
        constant_dict = {}
        if args.constant!='':
            constant_list = args.constant.split(',') 
            for item in constant_list:
                val = item.split('=')
                filename =''
                name=val[0]
                if len(val) > 1: 
                    filename=val[1]
                if os.path.isfile(filename):
                    try:
                        print("Using Constant: " + filename)
                        sys.stdout.flush()
                        numpy_val = np.load(filename)
                    except ValueError:
                        raise ValueError(
                            "Unable to load file: %s, ensure it is a numpy file." % filename)
                else:
                    if not (infile.endswith('.pb') or infile.endswith('.onnx') or infile.endswith('.tflite')):
                        raise ValueError(
                            "Can only generate constants with ONNX, TF 1.x, and TFLite, please use a numpy file."+filename)
                    # try:
                    from deepview_rtm.utils import gen_constant
                    numpy_val = gen_constant(
                        infile, args.input_shape, filename)
                    # except Exception:
                    #     raise ValueError("Unable to generate constant, ensure %s is a layer in the model "
                    #                     "or use a numpy file.")
                if name == 'ssd_anchor_boxes':
                    constant_dict[name] = numpy_val.reshape(-1,4).copy()
                else:
                    constant_dict[name] = numpy_val

        if args.save_map == '':
            save_map = None
        else:
            save_map = args.save_map

        if args.no_map:
            mem_map = False
        else:
            mem_map = True

        if args.save_layers == None or args.save_layers == []:
            save_layers = []
        else:
            save_layers = args.save_layers

        if args.copy_layers == None or args.copy_layers == []:
            copy_layers = []
        else:
            copy_layers = []
            copy_args = args.copy_layers
            if len(copy_args) % 2 != 0:
                raise ValueError("There must be an even number of layers")
            for i in range(0, len(copy_args), 2):
                copy_layers.append((copy_args[i], copy_args[i + 1]))

        if args.labels == '' or args.labels == [] or args.labels == None:
            labels = None
        elif os.path.isfile(args.labels):
            with open(args.labels, 'r') as f:
                labels = f.read().split('\n')
        else:
            labels = array = [v for v in args.labels.split(',')]   
            if not len(labels) > 0:
                print("Could not find provided labels file")
                raise FileNotFoundError

        if args.skip_optimizations == '' or args.skip_optimizations==[]:
            skip_optimizations = []
        else:
            skip_optimizations = args.skip_optimizations

        if args.panel_shuffle == 'none':
            panel_shuffle = None
        else:
            panel_shuffle = args.panel_shuffle

        user_ops = []
        if args.user_ops =='' or args.user_ops==['']:
            args.user_ops =None

        if args.user_ops is not None:
            for user in args.user_ops:
                print('Loading custom user_ops handler %s' % user)
                sys.path.append(os.path.dirname(user))
                user_mod = os.path.splitext(os.path.basename(user))[0]
                user_ops.append(__import__(user_mod))

        subgraph_names = []
        if args.input_names or args.output_names:
            if args.input_names is None or args.input_names == '':
                subgraph_names.append([])
            else:
                subgraph_names.append(args.input_names)
            if args.output_names is None or args.input_names == '':
                subgraph_names.append([])
            else:
                subgraph_names.append(args.output_names)

        try:
            from deepview_rtm.optimizer import DeepViewOptimizer

            #imports import file in memory as a graph
            optimizer = DeepViewOptimizer(infile,
                                        args.nnef_format,
                                        skip_optimizations,
                                        panel_shuffle,
                                        args.input_shape,
                                        user_ops,
                                        args.quantize,
                                        args.input_type,
                                        args.output_type,
                                        samples,
                                        args.num_samples,
                                        model_input_type,
                                        subgraph_names,
                                        args.quant_tensor,
                                        args.quant_channel,
                                        args.force_quant_tensor,
                                        args.quant_normalization,
                                        args.activation_datatype,
                                        args.transpose_conv_filter_datatype,
                                        onnx_input_format)
        except ImportError as e:
            return {
                'success': 'no',
                'message': "Unabled to import DeepViewOptimizer. "+str(e)
            }
        except Exception as err:
            if int(os.getenv("DEEPVIEW_CONVERTER_DEBUG", 0)) > 0:
                import traceback
                traceback.print_exc()
                print(sys.exc_info()[2])
                print(err.__traceback__)
                raise Exception("Debug: ").with_traceback(sys.exc_info()[2])
            return {
                'success': 'no',
                'message': 'Optimizer Error:'+ str(err)
            }


        try:
    
            from deepview_rtm.exporter_v1 import DeepViewExporter

            exporter = DeepViewExporter(optimizer, name=args.name, mem_map=mem_map,
                                        opt_map=args.optimize_map, save_map=save_map,
                                        save_layers=save_layers, copy_layers=copy_layers,
                                        svm=svm, ext_constants=constant_dict,
                                        labels=labels,
                                        input_names=input_names, output_names=output_names,
                                        user_ops=user_ops,
                                        normalization=args.normalization)                                        
            buffer = exporter.run()

            print("Saving File")

            with open(outfile, 'wb') as f:
                f.write(buffer)
        except ImportError as e:
            return {
            'success': 'no',
            'message': 'Unable to import DeepViewExporter. '+str(e) 
            }
        except Exception as err:
            if int(os.getenv("DEEPVIEW_CONVERTER_DEBUG", 0)) > 0:
                import traceback
                traceback.print_exc()
                print(sys.exc_info()[2])
                print(err.__traceback__)
                raise Exception("Debug: ").with_traceback(sys.exc_info()[2])
            return {
                'success': 'no',
                'message': 'Conversion Error:'+ str(err)
            }

           
        return {
            'success': 'yes',
            'message': 'Converted'
        }

    except Exception as e:
        return {
            'success': 'no',
            'message': str(e)
        }

#  ------------------------------------  Private Functions ---------------------------------------------
def __get_source_type(infile):
    src = ""
    try:
        if os.path.isfile(infile):
            src = os.path.splitext(infile)[1]
            src = src.replace('.', '')
        else:   # it is a dir
            #check for saved model
            for fname in os.listdir(infile):
                if os.path.splitext(fname)[1] == '.pb':
                    src = 'pb'
    except Exception as e:
        print(e)
        src=''
    return src
    

