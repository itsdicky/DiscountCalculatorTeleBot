import logging
from script import calculateDiscount
from telegram import Update
from telegram.ext import (
  Application,
  CommandHandler,
  ContextTypes,
  ConversationHandler,
  MessageHandler,
  filters,
)

# from script import calculateDiscount

logging.basicConfig(
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  level=logging.INFO)
logger = logging.getLogger(__name__)

PRICE, DISC, DELIV, MAXDISC, SERVICE, RESULT = range(6)

data = {}
prices = []


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  custom_keyboard = [['start', 'cancel']]
  # intro
  await update.message.reply_text(
    "Hi! My name is Discount Calculator Bot. I will hold a conversation with you."
  )
  await update.message.reply_text("Enter the price...")

  return PRICE


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  if update.message.text == 'next':
    await update.message.reply_text("Enter the discount percentage...")
    return DISC
  else:
    prices.append(int(update.message.text))
    logger.info("Price : %s", update.message.text)
    data['price'] = prices
    return PRICE


async def discount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  data['discount'] = int(update.message.text)
  logger.info("Discount : %s", update.message.text)
  await update.message.reply_text("Enter the delivery fee...")

  return DELIV


async def delivery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  data['delivery'] = int(update.message.text)
  logger.info("Delivery : %s", update.message.text)
  await update.message.reply_text("Enter the maximum discount...")

  return MAXDISC


async def maxDiscount(update: Update,
                      context: ContextTypes.DEFAULT_TYPE) -> int:
  data['maxdisc'] = int(update.message.text)
  logger.info("Maximum discount : %s", update.message.text)
  await update.message.reply_text("Enter the service fee...")

  return SERVICE


async def service(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  data['service'] = int(update.message.text)
  logger.info("Service : %s", update.message.text)
  await update.message.reply_text(
    # "Thank you! I hope we can talk again some day."
    calculateDiscount(data['price'], data['discount'], data['delivery'],
                      data['maxdisc'], data['service']))

  return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Cancels and ends the conversation."""
  user = update.message.from_user
  logger.info("User %s canceled the conversation.", user.first_name)
  await update.message.reply_text("Bye! I hope we can talk again some day.",
                                  reply_markup=ReplyKeyboardRemove())

  return ConversationHandler.END


if __name__ == '__main__':
  application = Application.builder().token(
    "5463276574:AAEKRbCTolTHG5Wm2qujbh7Wsmkdt4kBTpw").build()

  conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
      PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, price)],
      DISC: [MessageHandler(filters.TEXT & ~filters.COMMAND, discount)],
      DELIV: [MessageHandler(filters.TEXT & ~filters.COMMAND, delivery)],
      MAXDISC: [MessageHandler(filters.TEXT & ~filters.COMMAND, maxDiscount)],
      SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, service)],
      RESULT: [MessageHandler(filters.TEXT & ~filters.COMMAND, service)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
  )

  application.add_handler(conv_handler)

  application.run_polling()
