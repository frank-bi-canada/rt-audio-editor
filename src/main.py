from AudioProcessor import AudioProcessor

def main():
    audio_processor = AudioProcessor(sample_rate=24000, block_size=512)
    audio_processor.run()

if __name__ == '__main__':
    main()
