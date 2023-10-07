# DarkEye
# Global Surviellience Toolkit
#
# This product includes IP2Location LITE data available from http://www.ip2location.com.



from abc import abstractmethod
import os
import requests



class Credential:
    """
    Credential class
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __init__(self, username, password, link, passwordField, usernameField, method):
        self.username = username
        self.password = password
        self.link = link
        self.passwordField = passwordField
        self.usernameField = usernameField
        self.method = method

    def __str__(self):
        return f"{self.username}:{self.password}@{self.link}"

    def login(self):
        """
        Login method
        """
        self.session = requests.Session()
        if self.method == "POST":
            data = {
                self.usernameField: self.username,
                self.passwordField: self.password
            }
            r = self.session.post(self.link, data=data)
        elif self.method == "GET":
            r = self.session.get(self.link, params={
                self.usernameField: self.username,
                self.passwordField: self.password
            })
        else:
            raise ValueError("Method not supported.")
        return self.session


class SensorAction:
    """
    SensorAction class
    """

    def __init__(self, link, fields, values, method):
        self.link = link
        self.fields = fields
        self.values = values
        self.method = method

    def __str__(self):
        return f"{self.sensor}:{self.action}"


    def execute(self):
        """
        Execute method
        """
        if self.method == "POST":
            r = requests.post(self.link, data={
                self.fields: self.values
            })
        elif self.method == "GET":
            r = requests.get(self.link, params={
                self.fields: self.values
            })
        else:
            raise ValueError("Method not supported.")
        return r

    def execute(self, session):
        """
        Execute method
        """
        if self.method == "POST":
            r = session.post(self.link, data={
                self.fields: self.values
            })
        elif self.method == "GET":
            r = session.get(self.link, params={
                self.fields: self.values
            })
        else:
            raise ValueError("Method not supported.")
        return r


class Data:
    def __init__(self, timestamp, sensor, action):
        self.timestamp = timestamp
        self.sensor = sensor
        self.action = action

    def __str__(self):
        return f"{self.timestamp}:{self.sensor}:{self.action}"

    @abstractmethod
    def store(self, path):
        pass



class Sensor:

    def __init__(self, credential, actions):
        self.credential = credential
        self.actions = actions
    
    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def get_value(self):
        pass

    @abstractmethod
    def get_unit(self):
        pass

    @abstractmethod
    def get_timestamp(self):
        pass

    @abstractmethod
    def get_location(self):
        pass

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_status(self):
        pass



class Image(Data):
    def __init__(self, timestamp, sensor, action, image):
        super().__init__(timestamp, sensor, action)
        self.image = image

    def store(self, path):
        outputPath = os.path.join(path, self.sensor, self.action, self.timestamp + ".jpg")
        with open(outputPath, "wb") as f:
            f.write(self.image)



class Camera(Sensor):

    def __init__(self, address):
        self.address = address


class ExacqVisionWebcam():
    """
    ExacqVisionWebcam class
    """

    def __init__(self, address):
        self.address = address

    def get_data(self):
        pass

    def get_name(self):
        pass

    def get_type(self):
        pass

    def get_value(self):
        pass

    def get_unit(self):
        pass

    def get_timestamp(self):
        pass

    def get_location(self):
        pass

    def get_description(self):
        pass

    def get_status(self):
        pass
