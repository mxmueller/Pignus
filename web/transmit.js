window.connectionToPython = function () {
    eel.connection(Math.floor(Date.now() / 1000))(function (ret) {
        console.info(ret);
    });
    return true;
}

saltingReqPythonCall = function () {
    let passwordString = document.getElementById('textPassword').value,
        saltRange = $('#saltRange').find(":selected").attr('value')
    enforceSaltRange = document.getElementById('enforceSaltRange').checked

    console.info(passwordString, saltRange, enforceSaltRange, connectionToPython())

    eel.saltPasswordButtonPress(passwordString, saltRange, enforceSaltRange)(function (ret) {
        
        $('.saltedPassword').empty()
        $('.saltedPassword').append(ret)
    });
}

passwordReqPythonCall = function () {
    let length = document.getElementById('lenght').value,
        caps = document.getElementById('caps').checked,
        salt = document.getElementById('salt').checked

    console.info(length, caps, connectionToPython())

    eel.passwordButtonPress(length, caps)(function (ret) {
        $('.textPassword').empty()
        $('.textPassword').append(ret)

        if (salt)
            saltingReqPythonCall()
    });
}
