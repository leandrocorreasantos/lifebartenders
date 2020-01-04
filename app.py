from lifebartenders import app

if __name__ == '__main__':
    app.run(debug=app.debug, threaded=True, host='0.0.0.0', port=5000)
