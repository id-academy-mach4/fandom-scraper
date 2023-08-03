import tensorflow as tf
import numpy as np
import os
import time

path_to_file = ('data/celestegame.txt')
text = open(path_to_file, 'rb').read().decode(encoding='utf-8')
print(text[:250])

vocab = sorted(set(text))
chars = text
ids_from_chars = tf.keras.layers.StringLookup(
    vocabulary=list(vocab), mask_token=None)
ids = ids_from_chars(chars)
chars_from_ids = tf.keras.layers.StringLookup(
    vocabulary=ids_from_chars.get_vocabulary(), invert=True, mask_token=None)

chars = chars_from_ids(ids)
# Add your print statement below.
print(chars)
def text_from_ids(ids):
    return tf.strings.reduce_join(chars_from_ids(ids))

print(text_from_ids(ids))
all_ids = ids_from_chars(tf.strings.unicode_split(text, 'UTF-8'))
# Add your print statement here:
print(all_ids)
ids_dataset = tf.data.Dataset.from_tensor_slices(all_ids)
# Fill in the take function below
for ids in ids_dataset.take(500):
    print(chars_from_ids(ids).numpy().decode('utf-8'))
seq_length = 100
examples_per_epoch = len(text) // (seq_length + 1)
sequences = ids_dataset.batch(seq_length+1, drop_remainder=True)
# Write your for loop here
for sequence in sequences.take(1):
    print(chars_from_ids(sequence))

# Write your for loop here
for sequence in sequences.take(5):
    print(text_from_ids(sequence).numpy())

def split_input_target(sequence):
    input_text = sequence[:-1]
    target_text = sequence[1:]
    return input_text, target_text
example_text = "The quick brown fox jumps over the lazy dog."
print(split_input_target(list(example_text)))
dataset = sequences.map(split_input_target)
for input_example, target_example in dataset.take(1):
    print("Input :", text_from_ids(input_example).numpy())
    print("Target:", text_from_ids(target_example).numpy())
BATCH_SIZE =  64
BUFFER_SIZE =  10000
dataset = (
    dataset
    .shuffle(BUFFER_SIZE)
    .batch(BATCH_SIZE, drop_remainder=True)
    .prefetch(tf.data.experimental.AUTOTUNE))
# Add your print statement here
print(dataset)
vocab_size = len(vocab)
embedding_dim =  256
rnn_units = 2000
class MyModel(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim, rnn_units):
        super().__init__(self)
        self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
        self.gru = tf.keras.layers.GRU(rnn_units,
                                       return_sequences=True,
                                       return_state=True)
        self.dense = tf.keras.layers.Dense(vocab_size)

    def call(self, inputs, states=None, return_state=False, training=False):
        x = inputs
        x = self.embedding(x, training=training)
        if states is None:
            states = self.gru.get_initial_state(x)
        x, states = self.gru(x, initial_state=states, training=training)
        x = self.dense(x, training=training)

        if return_state:
            return x, states
        else:
            return x

model = MyModel(
        vocab_size=len(ids_from_chars.get_vocabulary()),
        embedding_dim=embedding_dim,
        rnn_units=rnn_units,)
from keras.layers import Input

for input_example_batch, target_example_batch in dataset.take(1):
    example_batch_predictions = model(input_example_batch)
    print(example_batch_predictions.shape, "(batch_size, sequence_length, vocab_size)")


#print(example_batch_predictions.shape)
# print(np.array([64,100,vocab_size]).shape)
input_0 = (64, 100)
model.build(input_0)
#model.build(Input(batch_shape=(64,100,vocab_size)))
# Add code to see the model summary below:
print(model.summary())
sampled_indices = tf.random.categorical(example_batch_predictions[0], num_samples=1)
sampled_indices = tf.squeeze(sampled_indices, axis=-1).numpy()

print("Input:\n", text_from_ids(input_example_batch[0]).numpy())
print("\nNext Char Predictions:\n", text_from_ids(sampled_indices).numpy())
# The line to set the  loss function
loss = tf.losses.SparseCategoricalCrossentropy(from_logits=True)
# Get an example batch mean loss
# example_batch_mean_loss = loss(target_example_batch, example_batch_predictions)

# # Add a print statment to print the shape of example_batch_predictions
# print(example_batch_predictions.shape)
# print("^ # (batch_size, sequence_length, vocab_size)")

# # Add a print statement to print example_batch_mean_loss
# print(example_batch_mean_loss)

# # Print the exponential of the average loss
# print("Exponential of average loss: ", tf.exp(example_batch_mean_loss).numpy())
model.compile(optimizer='adam', loss=loss)
#checkpoint_dir = './training_checkpoints'
#checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}")
#checkpoint_callback = tf.keras.callbacks.ModelCheckpoint( filepath=checkpoint_prefix, save_weights_only=True)
EPOCHS = 75
history = model.fit(dataset, epochs=EPOCHS)#, callbacks=[checkpoint_callback])
class OneStep(tf.keras.Model):
  def __init__(self, model, chars_from_ids, ids_from_chars, temperature=1.0):
    super().__init__()
    # Set your arguments
    self.temperature = temperature
    self.model = model
    self.chars_from_ids = chars_from_ids
    self.ids_from_chars = ids_from_chars

    # Create a mask to prevent "UNK" from being generated
    skip_ids = self.ids_from_chars(['[UNK]'])[:, None]
    sparse_mask = tf.SparseTensor(
      #Put an -inf at each bad index
      values=[-float('inf')]*len(skip_ids),
      indices=skip_ids,
      # Match the shape to the vocabulary
      dense_shape=[len(ids_from_chars.get_vocabulary())])

    #Add the prediction mask to the model
    self.prediction_mask = tf.sparse.to_dense(sparse_mask)

  @tf.function
  def generate_one_step(self, inputs, states=None):

    # Convert strings into token ids
    input_chars = tf.strings.unicode_split(inputs, 'UTF-8')
    input_ids = self.ids_from_chars(input_chars).to_tensor()

    # Use the rnn model on the inputs
    predicted_logits, states = self.model(inputs=input_ids, states=states, return_state=True)

    # Only use the last prediction
    predicted_logits = predicted_logits[:, -1, :]

    # Adjust using temperature
    predicted_logits = predicted_logits/self.temperature

    # Apply your prediction mask
    predicted_logits = predicted_logits

    # Sample the output to generate ids
    predicted_ids = tf.random.categorical(predicted_logits, num_samples=1)
    predicted_ids = tf.squeeze(predicted_ids, axis=-1)

    # Convert from ids back to chars
    predicted_chars = self.chars_from_ids(predicted_ids)

    # Return the predicted chars and states
    return predicted_chars, states


def summarize_article(keyword):
    # Generate a "one step" model using this class and your model from above
    one_step_model = OneStep(model, chars_from_ids, ids_from_chars)
    # Initialize the states to None
    states = None
    # Add to or change the string in the square brackets
    next_char = tf.constant([keyword])
    result = [next_char]
    # Add a for loop for the amount of characters (1000 is a good number to start with)
    for n in range (1000):
      # Leave this line untouched
      next_char, states =  one_step_model.generate_one_step(next_char, states=states)
      # Append next_char to result
      result.append(next_char)
    result = tf.strings.join(result)
    print(result[0].numpy().decode('utf-8'), '\n\n' + '_'*80)
