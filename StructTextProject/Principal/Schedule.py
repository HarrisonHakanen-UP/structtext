from Principal.IniciandoAPartirDoBanco import CompararRespostasDasProvas
import schedule

schedule.every(10).seconds.do(CompararRespostasDasProvas)
#schedule.every().day.at("00:00").do(CompararRespostasDasProvas)


while True:
    schedule.run_pending()