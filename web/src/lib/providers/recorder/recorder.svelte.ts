import { constraints, supportedFormats } from '$lib/config/recorder';

class RecorderProvider {
	recorder: MediaRecorder | null = $state(null);
	recording = $state(false);
	chunks: Blob[] = $state([]);

	setRecorder(recorder: MediaRecorder | null) {
		this.recorder = recorder;
	}

	appendChunk(chunk: Blob) {
		this.chunks.push(chunk);
	}
	clearChunks() {
		this.chunks = [];
	}
	switchRecording(state: boolean) {
		this.recording = state;
	}

	clearAll() {
		this.clearChunks();
		this.switchRecording(false);
		this.setRecorder(null);
	}

	setProcessAudio(processAudio: ((audioFile: File) => Promise<void>) | null) {
		this.processAudio = processAudio;
	}
	processAudio: ((audioFile: File) => Promise<void>) | null = $state(null);
}

export const mediaRecorderProvider = new RecorderProvider();

export const initMediaRecorder = async () => {
	stopExistingStream();
	if (!navigator.mediaDevices) {
		alert('Your browser does not support media recording');
		return;
	}

	try {
		const stream = await navigator.mediaDevices.getUserMedia(constraints);
		const availableFormats = supportedFormats.filter((format) =>
			MediaRecorder.isTypeSupported(format)
		);

		if (availableFormats.length === 0) {
			console.error('No supported formats found');
			return;
		}

		console.log('Supported formats:', availableFormats);
		const selectedFormat = availableFormats[0];
		console.log('Selected format:', selectedFormat);

		const recorder = new MediaRecorder(stream, { mimeType: selectedFormat });
		mediaRecorderProvider.setRecorder(recorder);

		recorder.onstart = () => {
			console.log('recorder is starting');
			mediaRecorderProvider.switchRecording(true);
		};

		recorder.ondataavailable = (event) => {
			mediaRecorderProvider.appendChunk(event.data);
		};

		recorder.onstop = () => {
			console.log('recorder is stopping');
			const chunks = mediaRecorderProvider.chunks;
			const blob = new Blob(chunks, { type: selectedFormat });

			mediaRecorderProvider.clearChunks();
			const audioFile = new File([blob], 'recording.' + selectedFormat, { type: selectedFormat });

			if (!mediaRecorderProvider.processAudio) {
				console.log('No processAudio function provided');
				return;
			}

			mediaRecorderProvider.processAudio(audioFile);
			mediaRecorderProvider.switchRecording(false);
		};
	} catch (error) {
		console.error('User denied microphone:', error);
	}
};

const stopExistingStream = () => {
	const recorder = mediaRecorderProvider.recorder;
	if (recorder && recorder.state !== 'inactive') {
		console.log('Stopping existing recorder...');
		recorder.stop();
		recorder.stream.getTracks().forEach((track) => track.stop());
		mediaRecorderProvider.setRecorder(null);
	}
};
