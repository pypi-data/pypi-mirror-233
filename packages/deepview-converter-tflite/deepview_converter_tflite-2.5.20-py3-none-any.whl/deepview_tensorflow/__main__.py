from .conversion_tflite import convert_to_tflite
import numpy as np
import os, sys
from deepview.converter.plugin_api.args_processor import ArgsProcessor

params_ref = {
        'tflite-converter': {'type': 'string',   'choices': ['mlir','toco'], 'default':'mlir','group':'debug','public':True,
                'help':'Converter library to use'}
        }

params_h5_tflite = params_ref
params_onnx_tflite = params_ref
params_pb_tflite = params_ref

supported_outputs = ['tflite']
supported_inputs = ['onnx', 'pb', 'h5']

def query_convert(src_type, dst_type):
    try:

        if src_type is None or dst_type is None:
            return {
                'supported_inputs': [{'ext':'h5','name':'Keras'}, {'ext':'pb','name':'Tensorflow'},{'ext':'onnx','name':'ONNX'},{'ext':'http','name':'Web Hosted Model'}],
                'supported_outputs':[{'ext':'tflite','name':'Tensorflow Lite'}]
            }

        ref = None
        if dst_type != 'tflite':
            return None

        ref = params_pb_tflite

        return ref
    except:
        return None

def convert(infile, outfile, params):
    try:
        src_type=''
        dst_type=''
        if 'input-model-type' in params:
            src_type=params['input-model-type']
        if 'output-model-type' in params:
            dst_type = params['output-model-type']

        ref = query_convert(src_type, dst_type)
        if ref is None:
            return {
                'success': 'no',
                'message': 'Not Valid file formats'
            }

        args = ArgsProcessor()
        args.process(params,ref)

        samples = [args.samples, args.crop]
        
    except Exception as e:
        return {
            'success': 'no',
            'message': "ERROR:"+str(e)
        }

    try:
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

        convert_to_tflite(infile, outfile, args.input_shape,
                        args.quantize, samples, args.num_samples, model_input_type, args.input_type, 
                        args.output_type, input_names, output_names, args.quant_normalization,
                        args.quant_tensor, args.quant_channel,
                        args.tflite_converter)
        
        return {
            'success': 'yes',
            'message': 'Converted'
        }

    except Exception as e:
        if int(os.getenv("DEEPVIEW_CONVERTER_DEBUG", 0)) > 0:
            import traceback
            traceback.print_exc()
            print(sys.exc_info()[2])
            print(e.__traceback__)
            raise Exception("Debug: ").with_traceback(sys.exc_info()[2])
        else:
            return {
                'success': 'no',
                'message': str(e.args)
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
    except FileNotFoundError:
        src=''

    return src






