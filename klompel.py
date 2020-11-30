from auditok import ADSFactory, AudioEnergyValidator, StreamTokenizer, player_for
from auditok import workers
from auditok.cmdline_util import make_kwargs, initialize_workers
import logging
from parseargs import do_the_args_thing


def main():
    logger = logging.getLogger('KLOMPEL')

    args = do_the_args_thing([])

    kwargs = make_kwargs(args)
    reader, observers = initialize_workers(
        logger=logger, **kwargs.io, **kwargs.miscellaneous
    )
    tokenizer_worker = workers.TokenizerWorker(
        reader, observers, logger=logger, **kwargs.split
    )
    tokenizer_worker.start_all()



# asource = ADSFactory.ads(rec=True) #max_time ?
#
# # validator = AudioEnergyValidator(sample_width=asource.get_sample_width(), energy_threshold=50)
# validator = AudioEnergyValidator(sample_width=2, energy_threshold=50)
# tokenizer = StreamTokenizer(validator=validator, min_length=20, max_length=250, max_continuous_silence=30)
#
# player = player_for(asource)
#
# def echo(data, start, end):
#     print("Acoustic activity at: {0}--{1}".format(start, end))
#     player.play(''.join(data))
#
# asource.open()
#
# tokenizer.tokenize(asource, callback=echo)


if __name__ == '__main__':
    main()
