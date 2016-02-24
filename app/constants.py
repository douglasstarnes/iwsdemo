TICKET_STATUS_OPEN = 0
TICKET_STATUS_IN_PROGRESS = TICKET_STATUS_OPEN + 1
TICKET_STATUS_CLOSED = TICKET_STATUS_IN_PROGRESS + 1
TICKET_STATUS_ACCEPTED = TICKET_STATUS_CLOSED + 1

STATUS_MESSAGES = [
    {'message':'Open', 'button_title': 'Accept Ticket', 'next_status': 3},
    {'message':'In Progress', 'button_title': 'Close Ticket', 'next_status': 2},
    {'message':'Closed', 'next_status': -1},
    {'message':'Accepted', 'button_title': 'Begin Ticket', 'next_status': 1}
]
