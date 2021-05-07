import bz2

#decompress data
with bz2.open('gaze_tracking/trained_models/shape_predictor_68_face_landmarks.dat.bz2', 'rb') as f:
    uncompressed_content = f.read()

#store decompressed file
with open('gaze_tracking/trained_models/shape_predictor_68_face_landmarks.dat', 'wb') as f:
   f.write(uncompressed_content)
   f.close()