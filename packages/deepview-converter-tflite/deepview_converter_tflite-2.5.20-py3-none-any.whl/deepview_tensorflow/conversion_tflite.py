# Copyright 2018 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

import numpy as np
import os
import sys
import tarfile
from PIL import Image
import inspect

png = '.png'
jpg = '.jpg'
jpeg = '.jpeg'
onnx_file = '.onnx'
tflite_file = '.tflite'
h5_file = '.h5'
tfhub_ext = 'https://tfhub.dev/'
convert_message = "Converted from "
signed = 'signed'
unsigned = 'unsigned'


def always_false(converter):
    return False

def graph_def_from_saved_model(default_shape, model_dir, experimental_new_converter=True, allow_custom_ops=False,
                               quantize=False, input_type='float32', output_type='float32', dataset_gen=None,
                               dequantize=False, quant_tensor=False):
    import tensorflow as tf
    import tempfile
    if not os.path.isdir(model_dir):
        model_dir = os.path.dirname(model_dir)
    loaded = tf.saved_model.load(model_dir)
    in_shape_provided = True
    if list(loaded.signatures.keys()):
        in_shape = list(loaded.signatures[tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY].inputs[0].get_shape())
        if None in in_shape:
            in_shape_provided = False
    if not (list(loaded.signatures.keys())) or not in_shape_provided:
        print("WARNING, signature key not found or input shape not provided. \n"
              "Default shape is set to " + str(default_shape) + "\n"
                                                                "Change default shape using --default_shape")
        with tempfile.TemporaryDirectory() as temp:
            module_with_signature_path = temp
            if not os.path.exists(module_with_signature_path):
                os.mkdir(module_with_signature_path)
            # if quantize_format == 'int8':
            #     call = loaded.__call__.get_concrete_function(tf.TensorSpec(default_shape, tf.int8))
            # elif quantize_format == 'uint8':
            #     call = loaded.__call__.get_concrete_function(tf.TensorSpec(default_shape, tf.uint8))
            # else:
            call = loaded.__call__.get_concrete_function(tf.TensorSpec(default_shape, tf.float32))
            tf.saved_model.save(loaded, module_with_signature_path, signatures=call)
            converter = tf.lite.TFLiteConverter.from_saved_model(module_with_signature_path)
            if quantize:
                converter.optimizations = [tf.lite.Optimize.DEFAULT]
                converter.representative_dataset = dataset_gen
                if quant_tensor:
                    converter._experimental_disable_per_channel = True
                if input_type == 'int8':
                    converter.inference_input_type = tf.int8
                elif input_type == 'uint8':
                    converter.inference_input_type = tf.uint8
                if output_type == 'int8':
                    converter.inference_output_type = tf.int8
                elif output_type == 'uint8':
                    converter.inference_output_type = tf.uint8
            converter.experimental_new_converter = experimental_new_converter
            converter.allow_custom_ops = allow_custom_ops
            converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS]
            try:
                return converter.convert()
            except Exception as e:
                if quantize:
                    converter.experimental_new_quantizer = False
                    return converter.convert()
                else:
                    raise e
    else:
        converter = tf.lite.TFLiteConverter.from_saved_model(model_dir)
    if quantize:
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.representative_dataset = dataset_gen
        if quant_tensor:
            converter._experimental_disable_per_channel = True
        if input_type == 'int8':
            converter.inference_input_type = tf.int8
        elif input_type == 'uint8':
            converter.inference_input_type = tf.uint8
        if output_type == 'int8':
            converter.inference_output_type = tf.int8
        elif output_type == 'uint8':
            converter.inference_output_type = tf.uint8
    converter.experimental_new_converter = experimental_new_converter
    converter.allow_custom_ops = allow_custom_ops
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS]
    try:
        return converter.convert()
    except Exception as e:
        if quantize:
            converter.experimental_new_quantizer = False
            return converter.convert()
        else:
            raise e


def graph_def_from_tfhub_model(default_shape, model_handle, experimental_new_converter=True, allow_custom_ops=False,
                               quantize=False, model_input_type=np.float32, input_type='float32', output_type='float32', 
                               dataset_gen=None, dequantize=False, quant_tensor=False):
    """
    graph_def_from_tfhub_model(default_shape, model_handle, experimental_new_converter=True, allow_custom_ops=False,
                               quantize=False, input_type='float32', output_type='float32', dataset_gen=None,
                               dequantize=False)

    Converts a provided TFHub URL to TFLite and returns the buffer.

    Parameters
    ----------
    default_shape : list
        The default shape for the input to the provided TFHub Model.
    model_handle : string
        The TFHub URL of the desired model to be converted.
    experimental_new_converter : {True, False}, optional
        Whether to use TOCO or MLIR conversion to TFLite.
    allow_custom_ops : {True, False}, optional
        Whether to allow the use of custom operations within the TFLite Model.
    quantize : {True, False}, optional
        Whether to quantize the provided TFHub Model during conversion to TFLite.
    input_type : {'float32', 'int8', 'uint8'}, optional
        The datatype for input layers in the model during quantization to TFLite.
    output_type : {'float32', 'int8', 'uint8'}, optional
        The datatype for output layers in the model during quantization to TFLite.
    dataset_gen : function, optional
        The function that provides samples for quantization. If None is provided, 
        quantization is unavailable.
    dequantize : {True, False}, optional
        This parameter is obsolete and to be removed.

    Returns
    -------
    tflite_buffer : bytes
        The converted TFLite Model buffer.
    """
    # Loads a TF Hub model by converting to a keras model and prepending an input layer
    import tensorflow_hub as hub
    import tensorflow as tf
    assert float(tf.__version__[:2]) >= 2.0, \
        "Tensorflow 2.0 or greater is required for Tensorflow Hub models"
    print("Importing TF Hub model with shape: " + str(default_shape))
    print("If you want a different input size, specify a default shape using --default_shape")
    # if quantize_format == 'int8':
    #     keras_model = tf.keras.Sequential(
    #         [tf.keras.layers.InputLayer(input_shape=default_shape[1:], dtype=tf.int8),
    #         hub.KerasLayer(model_handle)])
    # elif quantize_format == 'uint8':
    #     keras_model = tf.keras.Sequential(
    #         [tf.keras.layers.InputLayer(input_shape=default_shape[1:], dtype=tf.uint8),
    #         hub.KerasLayer(model_handle)])
    # else:
    if model_input_type == np.float32:
        inputs = tf.keras.Input(shape=default_shape[1:], dtype=tf.float32)
    elif model_input_type == np.int8:
        inputs = tf.keras.Input(shape=default_shape[1:], dtype=tf.int8)
    elif model_input_type == np.uint8:
        inputs = tf.keras.Input(shape=default_shape[1:], dtype=tf.uint8)
    else:
        raise ValueError("We currently do not support input type: %s" % str(model_input_type))
    layers = hub.KerasLayer(model_handle)(inputs)
    keras_model = tf.keras.Model(inputs=inputs, outputs=layers)
    # keras_model = tf.keras.Sequential(
    #     [tf.keras.layers.InputLayer(input_shape=default_shape[1:]),
    #      hub.KerasLayer(model_handle)])
    converter = tf.lite.TFLiteConverter.from_keras_model(keras_model)
    if quantize:
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.representative_dataset = dataset_gen
        if quant_tensor:
            converter._experimental_disable_per_channel = True
        if input_type == 'int8':
            converter.inference_input_type = tf.int8
        elif input_type == 'uint8':
            converter.inference_input_type = tf.uint8
        if output_type == 'int8':
            converter.inference_output_type = tf.int8
        elif output_type == 'uint8':
            converter.inference_output_type = tf.uint8
    converter.experimental_new_converter = experimental_new_converter
    converter.allow_custom_ops = allow_custom_ops
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS]

    try:
        return converter.convert()
    except Exception as e:
        if quantize:
            converter.experimental_new_quantizer = False
            return converter.convert()
        else:
            raise e


def saved_model_exists(filename):
    """
    saved_model_exists(filename)

    Determines whether a filepath is a valid Saved Model file or directory.

    Parameters
    ----------
    filename : string
        The filepath to the Saved Model file/directory to be tested for validity.

    Returns
    -------
    valid : bool
        The validity of whether the file/directory is a Saved Model.
    """
    return os.path.isfile(filename + '/saved_model.pb') or \
           os.path.isfile(filename + '/saved_model.pbtxt') or \
           filename.endswith('saved_model.pb') or \
           filename.endswith('saved_model.pbtxt')


def convert_to_tflite(filename, outfile, default_shape,
                      quantize=False, samples='', num_samples=10, model_input_type=np.float32,
                      input_type='float32', output_type='float32', input_names=None,
                      output_names=None, quant_norm='unsigned', quant_tensor=False,
                      quant_channel=False, tflite_conv='mlir'):
    """
    convert_to_tflite(filename, outfile, default_shape, quantize=False, samples='', 
                      input_type='float32', output_type='float32', input_names=None, 
                      output_names=None, quant_norm='unsigned', tflite_conv='mlir')

​	 Converts the input model to TFLite. Provides the ability to quantize the model.


    Parameters
    ----------
    filename : str
        Specifies the path to a specific file or a TFHub URL of a given model that 
        is to be converted to TFLite.
    outfile : str
        The filepath of the output TFLite model.
    default_shape : list
​		The shape for the input layer of the model.
    quantize : {True, False}, optional
        If true, the model will be converted to a quantized TFLite model, if False 
        the model will remain in it's original datatype representation.
    samples : str, optional
        The location of dataset samples to be used for quantization. This can be a 
        filepath to a folder containing images or a URL to a datastore containing images.
    num_samples : int, optional
        The number of samples to use for quantization from a dataset.
    input_type : {'float32', 'int8', 'uint8', 'none'}, optional
        When quantizing a model to TFLite, this field allows you to select the datatype 
        for the input layers of the model. Using 'none' will maintain the default 
        datatype when converting to TFLite, otherwise the datatype entered will be the 
        input layer datatype.
    output_type : {'float32', 'int8', 'uint8', 'none'}, optional
        When quantizing a model to TFLite, this field allows you to select the datatype 
        for the output layers of the model. Using 'none' will maintain the default 
        datatype when converting to TFLite, otherwise the datatype entered will be the 
        output layer datatype.
    input_names : list, optional
        This field is only for use when converting to TFLite from a TF 1.x Protobuf file. 
        When a TF 1.x Protobuf file is being used, this field is mandatory and convert 
        the model to TFLite with the provided list of input names as the inputs to the 
        TFLite model. They must exist within the TF 1.x Protobuf model. This field has 
        no use for other model formats in conversion to TFLite.
    output_names : list, optional
        This field is only for use when converting to TFLite from a TF 1.x Protobuf file. 
        When a TF 1.x Protobuf file is being used, this field is mandatory and convert 
        the model to TFLite with the provided list of output names as the outputs in the 
        TFLite model. They must exist within the TF 1.x Protobuf model. This field has 
        no use for other model formats in conversion to TFLite.
    quant_norm : {'unsigned', 'signed'}, optional
        This field will determine the normalization used for images that will be used for 
        quantization. 'unsigned' will perform x / 255, 'signed' will perform (x / 127.5) - 1.
    tflite_conv : {'mlir', 'toco'}, optional
        This field signifies which TFLite Converter shall be used, between the MLIR and 
        TOCO converters.
    """
    tflite_model = None
    experimental_new_conv = True
    if tflite_conv == 'toco':
        experimental_new_conv = False
    orig_filename = filename
    representative_dataset_gen = None

    if type(filename) == str and \
            os.path.exists(filename) and \
            os.path.isfile(filename) and \
            tarfile.is_tarfile(filename):
        with tarfile.open(filename) as tar:
            filename = filename.replace(".tar.gz", "")
            filename = filename.replace(".tar.bz2", "")
            filename = filename.replace(".tar.xz", "")
            filename = filename.replace(".tgz", "")
            filename = filename.replace(".tar", "")
            print('EXTRACTING TAR FILE TO -> %s' % filename)
            tar.extractall(filename)
        if not os.path.exists(filename + '/saved_model.pb'):
            filename = filename + '/' + filename + '/saved_model'
        if not os.path.exists(filename + '/saved_model.pb'):
            raise ValueError("Unable to located 'saved_model.pb' file " \
                "within the provided tarfile. Please manually unzip " \
                "and convert using the directory that contains 'saved_model.pb'")

    if type(filename) != str:  # Ensure filename is a valid type
        from tensorflow.core.framework import graph_pb2
        if type(filename) != graph_pb2.GraphDef and type(filename) != bytes:
            raise ValueError(
                'filename parameter must be a string, GraphDef, or TFLite flatbuffer \
                    for conversion to TFLite: %s' % type(filename))

    if quantize:
        from deepview.converter.plugin_api.dataset import Dataset
        dataset = Dataset(samples,default_shape,quant_norm, num_samples, model_input_type)
        representative_dataset_gen = dataset.generator()

    # Handle Keras models
    if type(filename) == str and (filename.endswith(h5_file) or filename.endswith('.hdf5')):

        import traceback, sys

        try:
            import tensorflow as tf

            sub_class = tf.lite.TFLiteConverter
            parent_classes = list(reversed(list(inspect.getmro(sub_class))))
            parent_classes[1]._is_unknown_shapes_allowed = always_false
            import tensorflow_hub as hub
            # Handle Tensorflow 2.0
        except Exception as e:
            print("ERROR...")
            print(e.args)
            raise e


        if float(tf.__version__[:2]) >= 2.0:
            keras_model = tf.keras.models.load_model(filename, compile=False,
                                                     custom_objects={'KerasLayer': hub.KerasLayer})
            default_shape = keras_model.input.shape[:]
            if keras_model.input.shape[0] is None:
                default_shape = [1] + keras_model.input.shape[1:]
                new_inp = tf.keras.layers.Input(shape=keras_model.input.shape[1:], batch_size=(1))
                keras_model.layers.pop(0)
                new_outputs = keras_model(new_inp)

                keras_model = tf.keras.models.Model(
                    new_inp,
                    new_outputs
                )
            converter = tf.lite.TFLiteConverter.from_keras_model(keras_model)
        else:
            converter = tf.lite.TFLiteConverter.from_keras_model_file(filename)
        if quantize:
            from deepview.converter.plugin_api.dataset import Dataset
            dataset = Dataset(samples,default_shape,quant_norm, num_samples, model_input_type)
            representative_dataset_gen = dataset.generator()
            converter.optimizations = [tf.lite.Optimize.DEFAULT, tf.lite.OpsSet.SELECT_TF_OPS]
            converter.representative_dataset = representative_dataset_gen
            if quant_tensor:
                converter._experimental_disable_per_channel = True
            if input_type == 'int8':
                converter.inference_input_type = tf.int8
            elif input_type == 'uint8':
                converter.inference_input_type = tf.uint8
            if output_type == 'int8':
                converter.inference_output_type = tf.int8
            elif output_type == 'uint8':
                converter.inference_output_type = tf.uint8
        try:
            converter.experimental_new_converter = experimental_new_conv
            tflite_model = converter.convert()
        except Exception as e:
            if quantize:
                converter.experimental_new_quantizer = False
                tflite_model = converter.convert()
            else:
                raise e
    elif type(filename) == str and filename.endswith(onnx_file):
        import onnx
        import onnx_tf
        import tempfile
        import tensorflow as tf
        third_party_error = "ERROR: Third Party Conversion Issue"
        try:
            model = onnx.load(filename)
        except Exception:
            raise ValueError(third_party_error)

        try:
            tf_rep = onnx_tf.backend.prepare(model, logging_level="WARN", auto_cast=True)
        except Exception:
            raise ValueError(third_party_error)

        with tempfile.TemporaryDirectory() as temp:
            try:
                tf_rep.export_graph(temp)
            except Exception:
                raise ValueError(third_party_error)
            try:
                converter = tf.lite.TFLiteConverter.from_saved_model(temp)
            except Exception:
                raise ValueError(third_party_error)
            if quantize:
                converter.optimizations = [tf.lite.Optimize.DEFAULT]
                converter.representative_dataset = representative_dataset_gen
                if quant_tensor:
                    converter._experimental_disable_per_channel = True
                if input_type == 'int8':
                    converter.inference_input_type = tf.int8
                elif input_type == 'uint8':
                    converter.inference_input_type = tf.uint8
                if output_type == 'int8':
                    converter.inference_output_type = tf.int8
                elif output_type == 'uint8':
                    converter.inference_output_type = tf.uint8
            converter.experimental_new_converter = experimental_new_conv
            converter.allow_custom_ops = True
            try:
                tflite_model = converter.convert()
            except Exception as e:
                if quantize:
                    try:
                        converter.experimental_new_quantizer = False
                        tflite_model = converter.convert()
                    except Exception as e:
                        if 'toco' in str(e):
                            raise ValueError("TOCO Conversion fails, please try with MLIR")
                        else:
                            raise ValueError(third_party_error)
                else:
                    if 'toco' in str(e):
                        raise ValueError("TOCO Conversion fails, please try with MLIR")
                    else:
                        raise ValueError(third_party_error)

    # Handle saved model and TFHub input
    elif type(filename) == str and \
            (saved_model_exists(filename) or filename.startswith('https://tfhub.dev')):
        if filename.startswith('https://tfhub.dev') or os.path.isfile(filename + '/tfhub_module.pb'):
            tflite_model = graph_def_from_tfhub_model(default_shape, filename,
                                                      experimental_new_converter=experimental_new_conv,
                                                      quantize=quantize, model_input_type=model_input_type,
                                                      input_type=input_type,
                                                      output_type=output_type,
                                                      dataset_gen=representative_dataset_gen,
                                                      quant_tensor=quant_tensor)
        else:
            try:  # Saved Model
                tflite_model = graph_def_from_saved_model(default_shape, filename,
                                                          experimental_new_converter=experimental_new_conv,
                                                          quantize=quantize, input_type=input_type,
                                                          output_type=output_type,
                                                          dataset_gen=representative_dataset_gen,
                                                          quant_tensor=quant_tensor)
            except ValueError as e:  # TFHub
                if e.args[0] == "This converter can only convert a single ConcreteFunction. " \
                                "Converting multiple functions is under development.":
                    tflite_model = graph_def_from_tfhub_model(default_shape, filename,
                                                              experimental_new_converter=experimental_new_conv,
                                                              quantize=quantize, model_input_type=model_input_type,
                                                              input_type=input_type,
                                                              output_type=output_type,
                                                              dataset_gen=representative_dataset_gen,
                                                              quant_tensor=quant_tensor)
                else:
                    raise e

    # Handle TF 1.x models
    elif type(filename) == str and filename.endswith('.pb'):
        if not input_names or not output_names:
            raise ValueError("ERROR: To convert TensorFlow 1.x graphs to TFLite, "
                             "please provide the input and output names")
        import tensorflow as tf
        # Handle Tensorflow 2.0
        if float(tf.__version__[:2]) >= 2.0:
            converter = tf.compat.v1.lite.TFLiteConverter.from_frozen_graph(
                filename, input_names, output_names,
                input_shapes={input_names[0]: default_shape})
        else:
            converter = tf.lite.TFLiteConverter.from_frozen_graph(
                filename, input_names, output_names,
                input_shapes={input_names[0]: default_shape})
        if quantize:
            converter.optimizations = [tf.lite.Optimize.DEFAULT]
            converter.representative_dataset = representative_dataset_gen
            if quant_tensor:
                converter._experimental_disable_per_channel = True
            if input_type == 'int8':
                converter.inference_input_type = tf.int8
            elif input_type == 'uint8':
                converter.inference_input_type = tf.uint8
            if output_type == 'int8':
                converter.inference_output_type = tf.int8
            elif output_type == 'uint8':
                converter.inference_output_type = tf.uint8
        try:
            converter.experimental_new_converter = experimental_new_conv
            tflite_model = converter.convert()
        except Exception as e:
            if quantize:
                converter.experimental_new_quantizer = False
                tflite_model = converter.convert()
            else:
                raise e

    if tflite_model is None:
        raise ValueError("ERROR: Input file %s cannot be converted to TFLite. "
                         "Ensure that the input model is a TF 1.x or 2.x model or an ONNX model."
                         % filename)
    with open(outfile, 'wb') as f:
        f.write(tflite_model)
