STATUSES = {
    'SUCCESS': ":white_check_mark:",
    'CHECK': ":ballot_box_with_check:",
    'STOP': ":octagonal_sign:",
    'PAUSE': ":pause_button:",
    'RESUME': ":play_pause:",
    'ERROR': ":x:",
}


def message(status, msg):
    return f'{STATUSES[status]} **`{msg}`**'
