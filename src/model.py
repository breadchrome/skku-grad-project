import tensorflow as tf
import keras
import numpy as np

import config

class AttenLayer(keras.layers.Layer):
    def __init__(self, num_state, **kw):
        super(AttenLayer, self).__init__(**kw)
        self.num_state = num_state
    
    def build(self, input_shape):
        self.kernel = self.add_weight('kernel', shape=[input_shape[-1], self.num_state])
        self.bias = self.add_weight('bias', shape=[self.num_state])
        self.prob_kernel = self.add_weight('prob_kernel', shape=[self.num_state])

    def call(self, input_tensor):
        atten_state = tf.tanh(tf.tensordot(input_tensor, self.kernel, axes=1) + self.bias)
        logits = tf.tensordot(atten_state, self.prob_kernel, axes=1)
        prob = tf.nn.softmax(logits)
        weighted_feature = tf.reduce_sum(tf.multiply(input_tensor, tf.expand_dims(prob, -1)), axis=1)
        return weighted_feature

    # for saving the model
    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'num_state': self.num_state,})
        return config

class ModelConfig:

    @staticmethod
    def build_model(
        tags=config.TAGS,
        window_length=config.WINDOW_LENGTH,
        input_size=config.SUBCARRIERS * 2 if config.USE_PHASE else config.SUBCARRIERS,
        use_attention=config.MODEL_USE_ATTENTION,
        units_lstm=config.MODEL_UNITS_LSTM,
        units_attention=config.MODEL_UNITS_ATTENTION,
        learning_rate=config.TRAIN_LEARNING_RATE
        ):
        x = keras.Input(shape=(window_length, input_size))
        
        if use_attention:
            x_hidden = keras.layers.Bidirectional(keras.layers.LSTM(units=units_lstm, return_sequences=True))(x)
            x_hidden = AttenLayer(units_attention)(x_hidden)
        else:
            x_hidden = keras.layers.Bidirectional(keras.layers.LSTM(units=units_lstm))(x)

        y = keras.layers.Dense(len(tags), activation='softmax')(x_hidden)
        model = keras.Model(inputs=x, outputs=y)
        model.compile(
            optimizer = keras.optimizers.Adam(learning_rate=learning_rate),
            loss='categorical_crossentropy',
            metrics=['accuracy'])
        
        return model

    @staticmethod
    def load_model(model_path, use_attention=config.MODEL_USE_ATTENTION):
        if use_attention:
            model = keras.models.load_model(model_path, custom_objects={'AttenLayer': AttenLayer})
        else:
            model = keras.models.load_model(model_path)

        return model