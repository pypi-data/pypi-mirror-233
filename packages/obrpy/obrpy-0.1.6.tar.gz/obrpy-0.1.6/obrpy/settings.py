import pandas as pd
import os

def genSettings(self,situation=None,Calibration_df=None,Test_df=None) -> None:
    """ 
        Generate settings object out of the setting .xlxs template created before identifies the use given to the FOS 
        -> "Calibration" stands for calibration of the own sensor (see CalibrationTemplate() for more info)
        -> "Test" stands for general user of FOS sensor (see TestTemplate() for further information)

        * optional: situation:                      "Calibration" or "Test"
        * optional: Calibration_df (pd.Dataframe):  generate it from getSettingsTemplates() (it's easier)
        * optional: Test_df (pd.Dataframe):         generate it from getSettingsTemplates() (it's easier)
                            
    """

    # Clear settings
    self.settings = self.Settings(situation)

    # Add dataframes if specified
    self.settings.book = {
        'Calibration': Calibration_df if isinstance(Calibration_df, pd.DataFrame) else CalibrationTemplate(),
        'Test': Test_df if isinstance(Test_df, pd.DataFrame) else TestTemplate(self._getNewValuesFromOBRfiles())
    }


def getSettingsTemplates(self) -> tuple:

    """ 
        Return settings templates for user usage 
    
        * return: calibration_data(pd.Dataframe), test_data (pd.DataFrame)
    
    """

    # create the "Calibration" sheet
    calibration_data = CalibrationTemplate()

    # create the "Test" sheet
    new_values = self._getNewValuesFromOBRfiles() 
    test_data = TestTemplate(new_values)


    return calibration_data, test_data


def CalibrationTemplate() -> pd.DataFrame:
    """ 
        Generates a tempate datafreme used to generate the seetings for the calibration situation.
        In the calibration situation the microstrain (Delta eps) and temperature (Delta T) 
        are asumed to vary in a linerar way, and only one segment (from z_ini->x=0 to z_fin)
        of the fiber is subjected to these variations.

    """

    data = [
        ['Delta T = ','','+ ','','x [m]'],
        ['Delta eps = ','','+ ','','x [m]'],
        ['z_ini [m] =',''],
        ['z_fin [m] =','']
    ]
    df = pd.DataFrame(data)
    return df

def TestTemplate(new_values) -> pd.DataFrame:
    """ 
        Generates a template dataframe used to generate the seetings for a situation where 
        several measurements are performed during a process where some magnitudes vary e.g. 
        load, temperature, time, ...

        *param: new_values(list) 
    """
    
    columns = ['Units','xlabel','ylabel']
    df = pd.DataFrame(columns=columns, index=new_values)

    return df

def _getNewValuesFromOBRfiles(self) -> list:
    
    """ 
        Get the new values written in the OBRbook by the user.

    """

    df = self.obrfiles.create_book()

    # Get the column names
    column_names = df.columns.tolist()

    # Remove the old ones
    try:
        column_names.remove('ID')
        column_names.remove('filename')
        column_names.remove('date')
        column_names.remove('f')
        column_names.remove('z')
        column_names.remove('Data')
        return column_names
    
    except Exception as e:
        if 'list.remove(x): x not in list' == str(e):
            return list()
        else:
            raise e

    