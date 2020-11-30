from auditok import ADSFactory, AudioEnergyValidator, StreamTokenizer, player_for, dataset

# We set the `record` argument to True so that we can rewind the source
asource = ADSFactory.ads(filename=dataset.one_to_six_arabic_16000_mono_bc_noise, record=True)

validator = AudioEnergyValidator(sample_width=asource.get_sample_width(), energy_threshold=65)

# Default analysis window is 10 ms (float(asource.get_block_size()) / asource.get_sampling_rate())
# min_length=20 : minimum length of a valid audio activity is 20 * 10 == 200 ms
# max_length=4000 :  maximum length of a valid audio activity is 400 * 10 == 4000 ms == 4 seconds
# max_continuous_silence=30 : maximum length of a tolerated  silence within a valid audio activity is 30 * 30 == 300 ms
tokenizer = StreamTokenizer(validator=validator, min_length=20, max_length=400, max_continuous_silence=30)

asource.open()
tokens = tokenizer.tokenize(asource)

# Play detected regions back

player = player_for(asource)

# Rewind and read the whole signal
asource.rewind()
original_signal = []

while True:
   w = asource.read()
   if w is None:
      break
   original_signal.append(w)

original_signal = ''.join(original_signal)

print("Playing the original file...")
player.play(original_signal)

print("playing detected regions...")
for t in tokens:
    print("Token starts at {0} and ends at {1}".format(t[1], t[2]))
    data = ''.join(t[0])
    player.play(data)

assert len(tokens) == 8