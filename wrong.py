# METHODS

notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
def noteName(note):
    return notes[note % 12] + str(note // 12 - 1)

def nameNote(name):
    return 12 * (1 + int(name[-1])) + notes.index(name[:-1])

# MAIN HOE

#filename: name of file
#samplerate: sample rate, if nonstandard
#tuning: tuning note, alphabetic w/ octave or midi
#
#note: alphabetic notes are only sharp so far
def disp(filename, samplerate = 44100, tuning = None):
    from aubio import source, pitch
    from numpy import mean, std

    # READ SETUP

    unit = "cent"
    downsample = 1
    samplerate //= downsample
    
    win_s = 4096 // downsample # fft size
    hop_s = 512  // downsample # hop size

    s = source(filename, samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.8

    pitch_o = pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit(unit)
    pitch_o.set_tolerance(tolerance)

    pitches = []
    confidences = []

    # READING

    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        confidence = pitch_o.get_confidence()
        pitches += [pitch]
        confidences += [confidence]
        if read < hop_s: break

    # OUTPUT

    if type(tuning) is str:
        tuning = nameNote(tuning)
    
    mistakes = {}
    for i, pitch in enumerate(pitches):
        if confidences[i] > 0.1:
            correct = int(pitch + 0.5) #### CENT/MIDI ONLY ####
            if correct > 0:
              if not correct in mistakes:
                  mistakes[correct] = []
              mistakes[correct].append(pitch - correct)

    offset = 0
    if tuning != None:
        offset = mean(mistakes[tuning])
    means = {i:100 * (mean(mistakes[i]) - offset) for i in mistakes}
    stds = {i:100 * std(mistakes[i]) for i in mistakes}
    print({i:len(mistakes[i]) for i in sorted(mistakes)})
    return "\n".join([noteName(i) + ": " + "%.2f" % abs(means[i]) + " cents " + ["flat", "sharp"][means[i] > 0] + ", " + "%.2f" % stds[i] + " cents variation" for i in sorted(mistakes)])
