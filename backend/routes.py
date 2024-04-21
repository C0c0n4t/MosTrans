from data.db_session import sessions

from backend.application import application
from flask import render_template, request, redirect, Response, url_for

from recognition.text import extractor
from recognition.speech_to_text import speech_to_text

voice_text = ""


@application.route("/", methods=["GET"])
def index():
    """Website home page"""

    from data.models import Line, Station, PassengerFlow

    audio = "audio" in str(request.query_string)

    data = dict()
    data["lines"] = dict()
    for line in sessions["train_database"].query(Line).order_by(Line.name).all():
        data["lines"][line.name] = [station.name for station in
                                    sessions["train_database"].query(Station).filter_by(line_id=line.id).order_by(
                                        Station.name).all()]
    data["stations"] = [station.name for station in
                        sessions["train_database"].query(Station).order_by(Station.name).all()]

    if not request.query_string:
        return render_template("index.html", data=data, answer=None, unresolved_line=False)
    elif "date" in str(request.query_string) and "station_name" in str(request.query_string):
        date = request.args.get('date')
        station_name = request.args.get('station_name')
        station = sessions["train_database"].query(Station).filter_by(name=station_name).first()
        answer = sessions["train_database"].query(PassengerFlow).filter_by(station_id=station.id, ymd=date).first()
        if answer is not None:
            answer = answer.count
        return render_template("index.html", data=data, date=date, station=station_name, answer=answer,
                               unresolved_line=False)
    elif "text" in str(request.query_string) and request.args.get("text") or audio:
        if audio:
            global voice_text
            text = voice_text
            voice_text = ""
        else:
            text = request.args.get("text")

        unresolved_line = False

        station_name = extractor.extract_station(text)
        if sessions["train_database"].query(Station).filter(Station.name.icontains(station_name)).first() is None:
            station_name = extractor.extract_keyword_levenshtein(
                [station.name for station in sessions["train_database"].query(Station).all()], text)
        stations = sessions["train_database"].query(Station).filter(Station.name.icontains(station_name)).all()
        if len(stations) == 1:
            station_name = stations[0].name
        else:
            line_name = extractor.extract_line(text)
            if sessions["train_database"].query(Station).filter(Station.name.icontains(station_name)).first() is None:
                line_name = extractor.extract_keyword_levenshtein(
                    [line.name for line in sessions["train_database"].query(Line).all()], text)
            for station in stations:
                found = sessions["train_database"].query(Line).filter_by(id=station.line_id).first()
                if found and found.name == line_name:
                    station_name = station.name
                    break
            else:
                station_name = stations[0].name
                unresolved_line = True
        date = extractor.extract_date(text)
        station = sessions["train_database"].query(Station).filter_by(name=station_name).first()
        answer = sessions["train_database"].query(PassengerFlow).filter_by(station_id=station.id, ymd=date).first()

        print(date, station_name, answer)
        if answer is not None:
            answer = answer.count
        return render_template("index.html", data=data, date=date, station=station_name, answer=answer,
                               unresolved_line=unresolved_line)

    return redirect("/")


@application.route("/get_voice", methods=["POST"])
def get_voice():
    """Gets file and stores transcription in `voice_text` variable"""
    wav_file = request.files["audio"]
    wav_file.save("data/databases/recoding.wav")

    global voice_text
    voice_text = speech_to_text.convert_speech("data/databases/recoding.wav")
    return redirect("/")
