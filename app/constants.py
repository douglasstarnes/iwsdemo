TICKET_STATUS_OPEN = 0
TICKET_STATUS_IN_PROGRESS = TICKET_STATUS_OPEN + 1
TICKET_STATUS_CLOSED = TICKET_STATUS_IN_PROGRESS + 1
TICKET_STATUS_ACCEPTED = TICKET_STATUS_CLOSED + 1

STATUS_MESSAGES = [
    {'message':'Open', 'button_title': 'Accept Ticket', 'next_status': 3, 'log_message': 'Ticket Opened'},
    {'message':'In Progress', 'button_title': 'Close Ticket', 'next_status': 2, 'log_message': 'Ticket Started'},
    {'message':'Closed', 'next_status': -1, 'log_message': 'Ticket Closed'},
    {'message':'Accepted', 'button_title': 'Begin Ticket', 'next_status': 1, 'log_message': 'Ticket Accepted'}
]

TICKET_LOG_TYPE_COMMENT = 0
TICKET_LOG_TYPE_STATUS_CHANGE = 1
