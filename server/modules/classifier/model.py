import tensorflow as tf
import keras


class ModelConfig:

    @staticmethod
    def build_model(tags: int, window_length: int, input_size: int, units_lstm: int, learning_rate: float):
        x = keras.Input(shape=(window_length, input_size))

        x_hidden = keras.layers.Bidirectional(
            keras.layers.LSTM(units=units_lstm))(x)

        y = keras.layers.Dense(tags, activation='softmax')(x_hidden)
        model = keras.Model(inputs=x, outputs=y)
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
            loss='categorical_crossentropy',
            metrics=['accuracy'])

        return model

    @staticmethod
    def load_model(model_path):
        return keras.models.load_model(model_path)
