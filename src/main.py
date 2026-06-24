from AudioProcessor import AudioProcessor

def main():
    audio_processor = AudioProcessor(sample_rate=12000, block_size=1024)
    audio_processor.run()

if __name__ == '__main__':
    main()
