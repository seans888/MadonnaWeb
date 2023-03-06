import datetime
from Reservation.models import Facility, Reservations, Prices


def check_availability(Prices, checkIn, checkOut):
    avail_list=[]
    reservationList = Reservations.objects.filter(prices=Prices)
    print(reservationList)
    for reservation in reservationList:
        if reservation.checkIn > checkOut or reservation.checkOut<checkIn:
            avail_list.append(True)
        else:
            avail_list.append(False)

    return all(avail_list)


def check_availability2(Prices, checkIn, checkOut, timeIn, timeOut):
    avail_list=[]
    reservationList = Reservations.objects.filter(prices=Prices)
    print(reservationList)
    for reservation in reservationList:
        if reservation.checkIn > checkOut or reservation.checkOut<checkIn:
            avail_list.append(True)
        else:
            avail_list.append(False)

    return all(avail_list)