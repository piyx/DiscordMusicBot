class Emoji:
    Success = ":white_check_mark:"
    Check = ":ballot_box_with_check:"
    Stop = ":octagonal_sign:"
    Pause = ":pause_button:"
    Resume = ":play_pause:"
    Error = ":x:"


def beautify_message(emoji: Emoji, message: str):
    return f'{emoji} **`{message}`**'
