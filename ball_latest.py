from imutils.video import WebcamVideoStream



vs = WebcamVideoStream(src=0).start()


	frame = vs.read()
	frame = imutils.resize(frame, width=1280, height = 480)

vs.stop()
