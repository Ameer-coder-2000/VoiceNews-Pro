class BackgroundAudio {
    constructor() {
        this.audioContext = null;
        this.backgroundGain = null;
        this.voiceGain = null;
        this.isPlaying = false;
        this.oscillator = null;
        this.gainNode = null;
    }

    init() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.backgroundGain = this.audioContext.createGain();
            this.voiceGain = this.audioContext.createGain();
            
            // Set very low volume for background (15%)
            this.backgroundGain.gain.value = 0.15;
            this.voiceGain.gain.value = 1.0;
            
            // Connect nodes
            this.backgroundGain.connect(this.audioContext.destination);
            this.voiceGain.connect(this.audioContext.destination);
            
            return true;
        } catch (error) {
            console.log('Background audio not supported:', error);
            return false;
        }
    }

    startNewsAmbient() {
        if (!this.audioContext) {
            if (!this.init()) return;
        }

        this.stop(); // Stop any existing sound

        try {
            // Create a subtle news-style ambient sound using oscillators
            const now = this.audioContext.currentTime;
            
            // Create main ambient oscillator (low frequency, news-like)
            this.oscillator = this.audioContext.createOscillator();
            this.gainNode = this.audioContext.createGain();
            
            // Set frequency to a low, news-like hum (around 80 Hz)
            this.oscillator.frequency.setValueAtTime(80, now);
            this.oscillator.type = 'sine';
            
            // Create gentle fade-in
            this.gainNode.gain.setValueAtTime(0, now);
            this.gainNode.gain.linearRampToValueAtTime(0.1, now + 0.5);
            
            // Connect and start
            this.oscillator.connect(this.gainNode);
            this.gainNode.connect(this.backgroundGain);
            this.oscillator.start(now);
            
            // Add subtle modulation for more realistic sound
            const lfo = this.audioContext.createOscillator();
            const lfoGain = this.audioContext.createGain();
            lfo.frequency.value = 0.2; // Slow modulation
            lfoGain.gain.value = 5; // Small frequency variation
            
            lfo.connect(lfoGain);
            lfoGain.connect(this.oscillator.frequency);
            lfo.start(now);
            
            this.isPlaying = true;
            
        } catch (error) {
            console.log('Error starting ambient sound:', error);
        }
    }

    stop() {
        try {
            if (this.oscillator) {
                const now = this.audioContext.currentTime;
                this.gainNode.gain.linearRampToValueAtTime(0, now + 0.3);
                this.oscillator.stop(now + 0.3);
                this.oscillator = null;
                this.gainNode = null;
            }
            this.isPlaying = false;
        } catch (error) {
            console.log('Error stopping ambient sound:', error);
        }
    }

    fadeIn() {
        if (this.backgroundGain && this.isPlaying) {
            const now = this.audioContext.currentTime;
            this.backgroundGain.gain.linearRampToValueAtTime(0.15, now + 1.0);
        }
    }

    fadeOut() {
        if (this.backgroundGain && this.isPlaying) {
            const now = this.audioContext.currentTime;
            this.backgroundGain.gain.linearRampToValueAtTime(0.02, now + 0.5);
        }
    }
}

// Global instance
window.backgroundAudio = new BackgroundAudio();
