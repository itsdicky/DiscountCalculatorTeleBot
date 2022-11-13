import pandas as pd
import numpy as np


def calculateDiscount(price, disc_perc, deliv_price, max_disc, service):
  total_disc = sum(price) * disc_perc

  if total_disc > max_disc:
    fix_disc = max_disc
  else:
    fix_disc = total_disc

  disc_prop = []
  prop = []
  for i in price:
    disc_prop.append(round(i / sum(price) * fix_disc, 2))
    prop.append(round(i / sum(price) * 100, 2))

  price_after_disc = np.array(price) - np.array(disc_prop)
  deliv_fee = deliv_price / len(price)
  service_fee = service / len(price)
  pay_split = price_after_disc + deliv_fee + service_fee
  calculate_all = sum(pay_split)

  str_table = f'Berikut adalah detailnya:\nHarga: {price}\nProporsi: {prop}\nDiskon: {disc_prop}\nHarga setelah diskon: {price_after_disc}\nOngkir: {deliv_fee}\nBiaya layanan: {service_fee}\nBayar: {pay_split}\nJumlah: {calculate_all}'

  return str_table
