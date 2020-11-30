import io
import logging
import wave

import requests
from auditok import workers
from auditok.cmdline_util import make_kwargs, initialize_workers
from auditok.workers import Worker

from blinker import Blinker
from parseargs import do_the_args_thing


def main():
    logger = logging.getLogger('KLOMPEL')

    args = do_the_args_thing([])

    kwargs = make_kwargs(args)
    kwargs.split["min_dur"] = 0.5
    kwargs.split["drop_trailing_silence"] = True
    reader, observers = initialize_workers(
        logger=logger, **kwargs.io, **kwargs.miscellaneous
    )
    observers.append(EVPWorker())
    # observers.append(RegionSaverWorker(
    #     'Event_{id}_{start}-{end}_{duration:.3f}.wav',
    #     "wav"
    # ))
    tokenizer_worker = workers.TokenizerWorker(
        reader, observers, logger=logger, **kwargs.split
    )
    tokenizer_worker.start_all()

class EVPWorker(Worker):

    def __init__(self):
        self.blinker = Blinker()
        Worker.__init__(self)

    def _process_message(self, message):
        _, audio_region = message

        LOCAL = 'http://localhost:5000/api/audio'
        REMOTE = 'https://eurovision.qaware.de/api/audio'
        self.blinker.set_waiting()
        res = requests.post(url=REMOTE,
                            data=self.get_wav_bytes(message),
                            headers={'Content-Type': 'application/octet-stream'})
        if res.ok:
            result = res.json()
            intent = result["nlu_result"]["intent"]
            print(f"{intent}: {result['stt_result']['text']}")
            if intent == "TOI_OCC":
                self.blinker.set_occupied(True)
            elif intent == "TOI_FREE":
                self.blinker.set_occupied(False)
            else:
                self.blinker.restore()
        else:
            print("request failed")
            self.blinker.restore()


    def get_wav_bytes(self, message):
        audio_region = message[1]
        bytez = io.BytesIO()

        with wave.open(bytez, "wb") as fp:
            fp.setframerate(audio_region.sampling_rate)
            fp.setsampwidth(audio_region.sample_width)
            fp.setnchannels(audio_region.channels)
            fp.writeframes(audio_region._data)
        data = bytez.getvalue()
        bytez.close()
        return data

if __name__ == '__main__':
    main()
