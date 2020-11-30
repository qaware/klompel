from auditok import ADSFactory, AudioEnergyValidator, StreamTokenizer, player_for


def main():
    asource = ADSFactory.ads(rec=True) #max_time ?

    # validator = AudioEnergyValidator(sample_width=asource.get_sample_width(), energy_threshold=50)
    validator = AudioEnergyValidator(sample_width=2, energy_threshold=50)
    tokenizer = StreamTokenizer(validator=validator, min_length=20, max_length=250, max_continuous_silence=30)

    player = player_for(asource)

    def echo(data, start, end):
        print("Acoustic activity at: {0}--{1}".format(start, end))
        player.play(''.join(data))

    asource.open()

    tokenizer.tokenize(asource, callback=echo)


if __name__ == '__main__':
    main()
