""" keyw frame module """

import io
import os
import glob
import configparser
import wx
from KeywTextCtrl import KeywTextCtrl
from keyw_db import KeywDB


__version__ = '11.01.2023'
__author__ = 'Serhiy Kobyakov'


APP_DIR = ""
WORKING_DIR = ""
RELEASE_DIR = "~/"
SCALE_FACTOR = 1.
BORDER_IN = 3
BORDER_TOP = 3
TEXT_HEIGHT = 1
FNAME_STR_LENGTH = 1

DIR_BROWSER = 1
FILES_LIST = 2
IMAGE_PREVIEW = 3
# IMAGE_BITMAP = 4
ISOLATION_LISTBOX = 5
ISOLATION_EDIT = 6
MODEL_LISTBOX = 7
PROPERTY_LISTBOX = 8
TITLE_EDIT = 9
DESCR_EDIT = 10
CONCEPT_EDIT = 11
NEWS_EDIT = 12
ACTION_EDIT = 13
EMOTIONS_EDIT = 14
MODEL_SPEC_EDIT = 15
OBJECTS_EDIT = 16
IMAGE_SPEC_EDIT = 17
LOCATION_EDIT = 18
COMPOSITION_EDIT = 19
WWWWW_EDIT = 20
THE_REST_EDIT = 21

DB_SEARCH_EDIT = 30
DB_SEARCH_RESULTS = 31

STATUS_BAR = 40

MAIN_NOTEBOOK = 50

KEYW_FRAME = 100

# dispatcher object
kd = None

# database object
keyw_db = None


class BrowsePanel(wx.Panel):
    """The panel for browsing working dirctory"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        dir_ctrl = wx.DirPickerCtrl(self, DIR_BROWSER, style=wx.DIRCTRL_DEFAULT_STYLE)
        dir_ctrl.SetPath(WORKING_DIR)
        dir_ctrl.Bind(wx.EVT_DIRPICKER_CHANGED, self.do_list_files)
        self.files_list = wx.ListBox(self, FILES_LIST, style=wx.LB_SINGLE ^ wx.LB_HSCROLL)
        self.do_list_files(None)
        self.files_list.SetMinSize((FNAME_STR_LENGTH, -1))
        self.files_list.Bind(wx.EVT_LISTBOX, self.do_show_new_image)

        # Directory and file choose, leftmost vertical sizer
        file_sizer = wx.BoxSizer(wx.VERTICAL)
        file_sizer.Add(dir_ctrl, 0, wx.ALL | wx.EXPAND, BORDER_TOP)
        file_sizer.Add(self.files_list, 1, wx.ALL | wx.EXPAND, BORDER_TOP)

        file_sizer.Layout()
        self.SetSizerAndFit(file_sizer)

    def do_list_files(self, event):
        """ show list of jpegs in files list using actual working directory"""
        the_dir_picker = wx.FindWindowById(DIR_BROWSER)
        WORKING_DIR = the_dir_picker.GetPath()
        # print("Change working dir to:", WORKING_DIR)
        the_files = [os.path.basename(x) for x in glob.glob(os.path.join(WORKING_DIR, '*.jpg'))]
        the_listbox = wx.FindWindowById(FILES_LIST)
        the_listbox.Clear()
        if len(the_files) > 0:
            the_listbox.InsertItems(the_files, 0)

    def do_show_new_image(self, event):
        kd.show_image()



class ImagePanel(wx.Panel):
    """Image panel"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        # ---- image preview
        image_sizer = wx.BoxSizer(wx.HORIZONTAL)

        preview = wx.StaticBitmap(self, IMAGE_PREVIEW, size=(-1, -1))
        preview.SetMinSize((-1, FNAME_STR_LENGTH))
        image_sizer.Add(preview, 1, wx.ALL | wx.EXPAND, BORDER_IN)

        isolation_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Isolated on:')
        isolation_list = ['None', 'White', 'Black', ' other:']
        isolation_list_box = wx.ListBox(self, ISOLATION_LISTBOX, size=(-1, -1), choices=isolation_list,
                                             style=wx.LB_SINGLE)
        isolation_list_box.SetMinSize((FNAME_STR_LENGTH, -1))
        isolation_edit = KeywTextCtrl(self, ISOLATION_EDIT)
        isolation_edit.SetMinSize((FNAME_STR_LENGTH, TEXT_HEIGHT))
        isolation_sizer.Add(isolation_list_box, 1, wx.ALL | wx.EXPAND, BORDER_IN)
        isolation_sizer.Add(isolation_edit, 0, wx.ALL, BORDER_IN)
        image_sizer.Add(isolation_sizer, 0, wx.ALL | wx.EXPAND, BORDER_IN)

        model_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Model')
        model_list_box = wx.ListBox(self, MODEL_LISTBOX, size=(-1, -1), style=wx.LB_MULTIPLE)
        model_list_box.SetMinSize((FNAME_STR_LENGTH, -1))
        model_sizer.Add(model_list_box, 1, wx.ALL, BORDER_IN)
        image_sizer.Add(model_sizer, 0, wx.ALL | wx.EXPAND, BORDER_IN)

        property_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Property')
        property_list_box = wx.ListBox(self, PROPERTY_LISTBOX, size=(-1, -1), style=wx.LB_MULTIPLE)
        property_list_box.SetMinSize((FNAME_STR_LENGTH, -1))
        property_sizer.Add(property_list_box, 1, wx.ALL, BORDER_IN)
        image_sizer.Add(property_sizer, 0, wx.ALL | wx.EXPAND, BORDER_IN)

        image_sizer.Layout()
        self.SetSizerAndFit(image_sizer)


class TitleDescrPanel(wx.Panel):
    """Title and description panel"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        titles1_sizer = wx.FlexGridSizer(2, 2, BORDER_IN, BORDER_IN)
        title_label = wx.StaticText(self, label='Title', style=wx.ALIGN_RIGHT)
        title_label.SetMinSize((-1, TEXT_HEIGHT))
        description_label = wx.StaticText(self, label='Description', style=wx.ALIGN_RIGHT)
        # Set exact width of the 'Description' label:
        description_label.SetMinSize(description_label.GetTextExtent(description_label.GetLabel()))
        title_edit = KeywTextCtrl(self, TITLE_EDIT, allowComma=True)
        title_edit.SetMinSize((-1, TEXT_HEIGHT))
        description_edit = KeywTextCtrl(self, DESCR_EDIT, allowComma=True)
        description_edit.SetMinSize((-1, TEXT_HEIGHT))
        titles1_sizer.Add(title_label, 0, wx.EXPAND)
        titles1_sizer.Add(title_edit, 1, wx.ALL | wx.EXPAND, 0)
        titles1_sizer.Add(description_label, 0, wx.EXPAND)
        titles1_sizer.Add(description_edit, 1, wx.ALL | wx.EXPAND, 0)
        titles1_sizer.AddGrowableCol(1, 1)

        titles1_sizer.Layout()
        self.SetSizerAndFit(titles1_sizer)


class KeywPanel(wx.Panel):
    """Keywords panel"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        # ---- keywords input
        keyw_edit_sizer = wx.FlexGridSizer(11, 2, BORDER_IN, BORDER_IN)

        concept_label = wx.StaticText(self, label='Concept', style=wx.ALIGN_RIGHT)
        concept_edit = KeywTextCtrl(self, CONCEPT_EDIT)
        concept_edit.SetMinSize((FNAME_STR_LENGTH * 4, TEXT_HEIGHT))
        keyw_edit_sizer.Add(concept_label, 1, wx.EXPAND)
        keyw_edit_sizer.Add(concept_edit, 1, wx.EXPAND)

        news_label = wx.StaticText(self, label='News', style=wx.ALIGN_RIGHT)
        news_edit = KeywTextCtrl(self, NEWS_EDIT)
        news_edit.SetMinSize((FNAME_STR_LENGTH * 4, TEXT_HEIGHT))
        keyw_edit_sizer.Add(news_label, 1, wx.EXPAND)
        keyw_edit_sizer.Add(news_edit, 1, wx.EXPAND)

        action_label = wx.StaticText(self, label='Action', style=wx.ALIGN_RIGHT)
        action_edit = KeywTextCtrl(self, ACTION_EDIT)
        action_edit.SetMinSize((FNAME_STR_LENGTH * 4, TEXT_HEIGHT))
        keyw_edit_sizer.Add(action_label, 1, wx.EXPAND)
        keyw_edit_sizer.Add(action_edit, 1, wx.EXPAND)

        emotions_label = wx.StaticText(self, label='Emotions', style=wx.ALIGN_RIGHT)
        emotions_edit = KeywTextCtrl(self, EMOTIONS_EDIT)
        emotions_edit.SetMinSize((FNAME_STR_LENGTH * 4, TEXT_HEIGHT))
        keyw_edit_sizer.Add(emotions_label, 1, wx.EXPAND)
        keyw_edit_sizer.Add(emotions_edit, 1, wx.EXPAND)

        model_spec_label = wx.StaticText(self, label='Model-specific keywords', style=wx.ALIGN_RIGHT)
        model_spec_edit = KeywTextCtrl(self, MODEL_SPEC_EDIT)
        model_spec_edit.SetMinSize((FNAME_STR_LENGTH * 4, TEXT_HEIGHT))
        keyw_edit_sizer.Add(model_spec_label, 1, wx.EXPAND)
        keyw_edit_sizer.Add(model_spec_edit, 1, wx.EXPAND)

        objects_label = wx.StaticText(self, label='Objects', style=wx.ALIGN_RIGHT)
        objects_edit = KeywTextCtrl(self, OBJECTS_EDIT)
        objects_edit.SetMinSize((FNAME_STR_LENGTH * 4, TEXT_HEIGHT))
        keyw_edit_sizer.Add(objects_label, 1, wx.EXPAND)
        keyw_edit_sizer.Add(objects_edit, 1, wx.EXPAND)

        image_spec_label = wx.StaticText(self, label='Image-specific keywords', style=wx.ALIGN_RIGHT)
        image_spec_edit = KeywTextCtrl(self, IMAGE_SPEC_EDIT)
        image_spec_edit.SetMinSize((FNAME_STR_LENGTH * 4, TEXT_HEIGHT))
        keyw_edit_sizer.Add(image_spec_label, 1, wx.EXPAND)
        keyw_edit_sizer.Add(image_spec_edit, 1, wx.EXPAND)

        location_label = wx.StaticText(self, label='Location', style=wx.ALIGN_RIGHT)
        location_edit = KeywTextCtrl(self, LOCATION_EDIT)
        location_edit.SetMinSize((FNAME_STR_LENGTH * 4, TEXT_HEIGHT))
        keyw_edit_sizer.Add(location_label, 1, wx.EXPAND)
        keyw_edit_sizer.Add(location_edit, 1, wx.EXPAND)

        composition_label = wx.StaticText(self, label='Composition', style=wx.ALIGN_RIGHT)
        composition_edit = KeywTextCtrl(self, COMPOSITION_EDIT)
        composition_edit.SetMinSize((FNAME_STR_LENGTH * 4, TEXT_HEIGHT))
        keyw_edit_sizer.Add(composition_label, 1, wx.EXPAND)
        keyw_edit_sizer.Add(composition_edit, 1, wx.EXPAND)

        wwwww_label = wx.StaticText(self, label="Who? What? When? Where? Why?", style=wx.ALIGN_LEFT)
        wwwww_edit = KeywTextCtrl(self, WWWWW_EDIT)
        # Set exact width of the 'WWWWW' label:
        wwwww_label.SetMinSize(wwwww_label.GetTextExtent(wwwww_label.GetLabel()))
        wwwww_edit.SetMinSize((FNAME_STR_LENGTH * 4, TEXT_HEIGHT))
        keyw_edit_sizer.Add(wwwww_label, 0, 0)
        keyw_edit_sizer.Add(wwwww_edit, 0, wx.EXPAND)

        the_rest_label = wx.StaticText(self, label='The rest of words:', style=wx.ALIGN_RIGHT)
        the_rest_edit = KeywTextCtrl(self, THE_REST_EDIT, wrap=True)
        the_rest_edit.SetMinSize((FNAME_STR_LENGTH * 4, 3 * TEXT_HEIGHT))
        keyw_edit_sizer.Add(the_rest_label, 1, wx.EXPAND)
        keyw_edit_sizer.Add(the_rest_edit, 1, wx.EXPAND)

        keyw_edit_sizer.Layout()
        self.SetSizerAndFit(keyw_edit_sizer)


class MetadataPanel(wx.Panel):
    """Metadata panel"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        image_panel = ImagePanel(self)
        td_panel = TitleDescrPanel(self)
        keyw_panel = KeywPanel(self)
        browse_panel = BrowsePanel(self)
        the_button = wx.Button(self, id=wx.ID_ANY, label="Send data to DB and open next image")
        the_button.Bind(wx.EVT_BUTTON, self.do_save_data_open_next)

        metadata_sizer = wx.BoxSizer(wx.VERTICAL)
        metadata_sizer.Add(image_panel, 0, wx.ALL | wx.EXPAND, BORDER_IN)
        metadata_sizer.Add(td_panel, 0, wx.ALL | wx.EXPAND, BORDER_IN)
        metadata_sizer.Add(keyw_panel, 0, wx.ALL, BORDER_IN)
        metadata_sizer.Add(the_button, 0, wx.ALL | wx.ALIGN_RIGHT, BORDER_IN)
        metadata_sizer.Layout()

        # main sizer - to bring altogether
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(browse_panel, 0, wx.ALL | wx.EXPAND, BORDER_TOP)
        main_sizer.Add(metadata_sizer, 0, wx.ALL, BORDER_TOP)
        main_sizer.Layout()

        # set the size of the window
        self.SetSizerAndFit(main_sizer)

    def do_save_data_open_next(self, event):
        the_listbox = wx.FindWindowById(FILES_LIST)
        if the_listbox.GetSelection() > -1:
            kd.save_data()


class DatabasePanel(wx.Panel):
    """SQL database panel"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        the_sizer = wx.BoxSizer(wx.VERTICAL)

        db_search_edit = wx.TextCtrl(self, DB_SEARCH_EDIT, style=wx.TE_PROCESS_ENTER | wx.TE_MULTILINE)
        db_search_edit.SetMinSize((FNAME_STR_LENGTH * 4, TEXT_HEIGHT))
        db_search_edit.Bind(wx.EVT_TEXT_ENTER, self.search_DB_for_keywords)
        thumbnails_ctrl = wx.ListCtrl(self, DB_SEARCH_RESULTS, style=wx.LC_ICON)
        the_button = wx.Button(self, id=wx.ID_ANY, label="Populate the metadata fields")
        the_button.Bind(wx.EVT_BUTTON, self.on_button)

        the_sizer.Add(db_search_edit, 0, wx.ALL | wx.EXPAND, BORDER_IN)
        the_sizer.Add(thumbnails_ctrl, 1, wx.EXPAND, BORDER_IN)
        the_sizer.Add(the_button, 0, wx.ALL | wx.ALIGN_RIGHT, BORDER_IN)

        the_sizer.Layout()
        self.SetSizerAndFit(the_sizer)

        # self.Bind(wx.EVT_TEXT_ENTER, self.search_DB_for_keywords)

    def search_DB_for_keywords(self, event):
        kd.search_for_images_in_DB()

    def on_button(self, event):
        kd.populate_text_fields_using_search_results()


class KeywFrame(wx.Frame):
    def __init__(self, parent):
        # read variables from ini file:
        global APP_DIR
        APP_DIR = os.path.dirname(os.path.realpath(__file__))
        global WORKING_DIR
        WORKING_DIR = os.getcwd()
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(APP_DIR, 'keyw.ini'))
        global DEFAULT_DIR
        DEFAULT_DIR = self.config.get('keyw', 'DEFAULT_DIR', fallback=os.path.expanduser('~'))
        global RELEASE_DIR
        RELEASE_DIR = self.config.get('keyw', 'RELEASE_DIR', fallback=os.path.expanduser('~'))
        global SCALE_FACTOR
        SCALE_FACTOR = self.config.getfloat('keyw', 'SCALE_FACTOR', fallback=1.)
        # print("Scale factor:", SCALE_FACTOR)
        global BORDER_IN
        BORDER_IN = self.config.getint('keyw', 'BORDER_IN', fallback=1)
        global BORDER_TOP
        BORDER_TOP = self.config.getint('keyw', 'BORDER_TOP', fallback=1)
        # check if we get the variables successfully:
        # print('DEFAULT_DIR:', DEFAULT_DIR)

        # create DB object
        global keyw_db
        keyw_db = KeywDB(RELEASE_DIR)

        global KEYW_FRAME
        super().__init__(parent, title="Image keywords editor v." + __version__, id=KEYW_FRAME,
                         style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        the_panel = wx.Panel(self)

        # scale the app window using SCALE_FACTOR
        system_font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        the_panel.SetFont(system_font.Scale(SCALE_FACTOR))
        global TEXT_HEIGHT, FNAME_STR_LENGTH
        FNAME_STR_LENGTH, TEXT_HEIGHT = wx.Window.GetTextExtent(self, '2022-11-11_11-11-11_0000.jpg')
        TEXT_HEIGHT = round((TEXT_HEIGHT + 2) * SCALE_FACTOR)
        FNAME_STR_LENGTH = round(FNAME_STR_LENGTH * 1.15 * SCALE_FACTOR)

        # set the application icon
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(os.path.join(APP_DIR, "keyw.ico"), wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

        # create statusbar
        global STATUS_BAR
        self.status_bar = self.CreateStatusBar(1)

        notebook = wx.Notebook(the_panel, id=MAIN_NOTEBOOK)
        tab1 = MetadataPanel(notebook)
        tab2 = DatabasePanel(notebook)
        notebook.AddPage(tab1, "Metadata")
        notebook.AddPage(tab2, "Database search")

        sizer = wx.BoxSizer()
        sizer.Add(notebook, 1)
        sizer.SetSizeHints(self)

        the_panel.SetSizer(sizer)
        the_panel.SetSizerAndFit(sizer)

        # fix image preview min size
        # so it will not change later
        the_img_preview = wx.FindWindowById(IMAGE_PREVIEW)
        the_img_preview.SetMinSize(the_img_preview.GetSize())

        # create dispatcher object
        global kd
        kd = KeywDispatcher()


class KeywDispatcher:
    """dispatcher for keyw app"""
    the_frame = None
    files_list = None
    img_preview = None
    isolation_listbox = None
    isolation = None
    model_listbox = None
    property_listbox = None
    title = None
    descr = None
    concept = None
    news = None
    actions = None
    emotions = None
    model_spec = None
    objects = None
    image_spec = None
    location = None
    composition = None
    wwwww = None
    the_rest = None
    search_DB = None
    search_results = None
    main_notebook = None

    def __init__(self):
        self.the_frame = wx.FindWindowById(KEYW_FRAME)
        if not isinstance(self.the_frame, KeywFrame):
            print("Error: keyw app window wasn't initialized properly!")
            exit(1)
        self.files_list = wx.FindWindowById(FILES_LIST)
        self.img_preview = wx.FindWindowById(IMAGE_PREVIEW)
        self.isolation_listbox = wx.FindWindowById(ISOLATION_LISTBOX)
        self.isolation = wx.FindWindowById(ISOLATION_EDIT)
        self.model_listbox = wx.FindWindowById(MODEL_LISTBOX)
        self.property_listbox = wx.FindWindowById(PROPERTY_LISTBOX)
        self.title = wx.FindWindowById(TITLE_EDIT)
        self.descr = wx.FindWindowById(DESCR_EDIT)
        self.concept = wx.FindWindowById(CONCEPT_EDIT)
        self.news = wx.FindWindowById(NEWS_EDIT)
        self.actions = wx.FindWindowById(ACTION_EDIT)
        self.emotions = wx.FindWindowById(EMOTIONS_EDIT)
        self.model_spec = wx.FindWindowById(MODEL_SPEC_EDIT)
        self.objects = wx.FindWindowById(OBJECTS_EDIT)
        self.image_spec = wx.FindWindowById(IMAGE_SPEC_EDIT)
        self.location = wx.FindWindowById(LOCATION_EDIT)
        self.composition = wx.FindWindowById(COMPOSITION_EDIT)
        self.wwwww = wx.FindWindowById(WWWWW_EDIT)
        self.the_rest = wx.FindWindowById(THE_REST_EDIT)
        self.search_DB = wx.FindWindowById(DB_SEARCH_EDIT)
        self.search_results = wx.FindWindowById(DB_SEARCH_RESULTS)
        self.image_list = wx.ImageList(256, 256, mask=True)
        self.search_results.AssignImageList(self.image_list, wx.IMAGE_LIST_NORMAL)
        self.main_notebook = wx.FindWindowById(MAIN_NOTEBOOK)


    def show_image(self):
        """show new image"""
        if self.files_list.GetSelection() != -1:
            self.__clear_all_fields()
            fname = self.files_list.GetString(self.files_list.GetSelection())
            the_file = os.path.join(WORKING_DIR, fname)

            # downscale image to 256px and load it to preview
            data = open(the_file, "rb").read()
            the_image = wx.Image(io.BytesIO(data))
            the_w = the_image.GetWidth()
            the_h = the_image.GetHeight()
            # print(f"size: {the_w}x{the_h}")
            if the_w > the_h:
                w = 256
                h = round(256 * the_h / the_w)
            else:
                h = 256
                w = round(256 * the_w / the_h)

            # load image to preview
            the_bitmap = wx.Bitmap(the_image.Scale(w, h))
            the_img_preview = wx.FindWindowById(IMAGE_PREVIEW)
            the_img_preview.SetBitmap(the_bitmap)

            # load models and property releases for this day
            the_day = fname.split('_')[0]
            # print("models for the_day:", self.__get_models_list(the_day))
            models_for_the_day = self.__get_models_list(the_day)
            if len(models_for_the_day) > 0:
                self.model_listbox.InsertItems(models_for_the_day, 0)
            prop_for_the_day = self.__get_property_list(the_day)
            if len(prop_for_the_day) > 0:
                self.property_listbox.InsertItems(prop_for_the_day, 0)

            # if there is image data in DB - load it
            # else if there is metadata in the image - load it
            if not self.__get_image_data_from_DB(fname):
                self.__get_metadata_from_image()
            self.update_status()

    def update_status(self):
        """show actual information in statusbar"""
        status_str = self.files_list.GetString(self.files_list.GetSelection())
        self.the_frame.StatusBar.SetStatusText(status_str)

    def save_data(self):
        """when we are happy with the data - write it to DB and update the image"""
        # check if everything is allright within the data gathered in the text fields

        # write the data and select new image
        self.__write_to_db()
        self.__write_metadata_to_image()
        self.__select_next_image()

    def __get_image_data_from_DB(self, the_image: str) -> bool:
        img_data = keyw_db.get_img_data(the_image)
        if img_data is not None:
            # isolation
            if len(img_data[1]) == 0:
                self.isolation_listbox.SetSelection(0)
            else:
                self.isolation.AppendText(img_data[1])
                if img_data[1] == 'white':
                    self.isolation_listbox.SetSelection(1)
                elif img_data[1] == 'black':
                    self.isolation_listbox.SetSelection(2)
                else:
                    self.isolation_listbox.SetSelection(3)
            # model
            if len(img_data[2]) == 0:
                self.model_listbox.SetSelection(-1)
            else:
                models = img_data[2].split(', ')
                for model in models:
                    self.model_listbox.SetSelection(self.model_listbox.FindString(model))
            # property
            if len(img_data[3]) == 0:
                self.property_listbox.SetSelection(-1)
            else:
                models = img_data[3].split(', ')
                for model in models:
                    self.property_listbox.SetSelection(self.property_listbox.FindString(model))
            # text fields
            if len(img_data[4]) > 0:
                self.title.AppendText(img_data[4])
            if len(img_data[5]) > 0:
                self.descr.AppendText(img_data[5])
            if len(img_data[6]) > 0:
                self.concept.AppendText(img_data[6])
            if len(img_data[7]) > 0:
                self.news.AppendText(img_data[7])
            if len(img_data[8]) > 0:
                self.actions.AppendText(img_data[8])
            if len(img_data[9]) > 0:
                self.emotions.AppendText(img_data[9])
            if len(img_data[10]) > 0:
                self.model_spec.AppendText(img_data[10])
            if len(img_data[11]) > 0:
                self.objects.AppendText(img_data[11])
            if len(img_data[12]) > 0:
                self.image_spec.AppendText(img_data[12])
            if len(img_data[13]) > 0:
                self.location.AppendText(img_data[13])
            if len(img_data[14]) > 0:
                self.composition.AppendText(img_data[14])
            if len(img_data[15]) > 0:
                self.wwwww.AppendText(img_data[15])
            if len(img_data[16]) > 0:
                self.the_rest.AppendText(img_data[16])
            return True
        else:
            return False


    def __get_metadata_from_image(self):
        pass

    def __get_models_list(self, the_day: str):
        all_mr_jpg = glob.glob(os.path.join(RELEASE_DIR, 'Models', '*.jpg'))
        all_models_jpg = [os.path.basename(x).split('.')[0][11:] for x in all_mr_jpg if x.find(the_day) > 0]
        all_mr_pdf = glob.glob(os.path.join(RELEASE_DIR, 'Models', '*.pdf'))
        all_models = [os.path.basename(x).split('.')[0][11:] for x in all_mr_pdf if x.find(the_day) > 0]
        if len(all_models) > 0 and len(all_models_jpg) > 0:
            models = list(set(all_models.extend(all_models_jpg)))
        elif len(all_models) == 0 and len(all_models_jpg) > 0:
            models = all_models_jpg
        elif len(all_models) > 0 and len(all_models_jpg) == 0:
            models = all_models
        else:
            models = []
        if len(models) > 0:
            models = [model.replace('_', ' ') for model in models]
        return models

    def __get_property_list(self, the_day: str):
        all_mr_jpg = glob.glob(os.path.join(RELEASE_DIR, 'Properties', '*.jpg'))
        all_owners_jpg = [os.path.basename(x).split('.')[0][11:] for x in all_mr_jpg if x.find(the_day) > 0]
        all_mr_pdf = glob.glob(os.path.join(RELEASE_DIR, 'Properties', '*.pdf'))
        all_owners = [os.path.basename(x).split('.')[0][11:] for x in all_mr_pdf if x.find(the_day) > 0]
        if len(all_owners) > 0 and len(all_owners_jpg) > 0:
            owners = list(set(all_owners.extend(all_owners_jpg)))
        elif len(all_owners) == 0 and len(all_owners_jpg) > 0:
            owners = all_owners_jpg
        elif len(all_owners) > 0 and len(all_owners_jpg) == 0:
            owners = all_owners
        else:
            owners = []
        if len(owners) > 0:
            owners = [owner.replace('_', ' ') for owner in owners]
        return owners


    def __select_next_image(self):
        """ select next image"""
        if self.files_list.GetSelection() == self.files_list.GetCount() - 1:
            print("Done working!")
            exit(0)
        else:
            # select new element
            self.files_list.SetSelection(self.files_list.GetSelection() + 1)
            # post event so listbox'es internal function can take care of showing new image
            wx.PostEvent(self.files_list.GetEventHandler(), wx.PyCommandEvent(wx.EVT_LISTBOX.typeId, FILES_LIST))

    def __clear_all_fields(self):
        self.isolation_listbox.SetSelection(-1)
        self.isolation.Clear()
        self.model_listbox.SetSelection(-1)
        self.model_listbox.Clear()
        self.property_listbox.SetSelection(-1)
        self.property_listbox.Clear()
        self.title.Clear()
        self.descr.Clear()
        self.concept.Clear()
        self.news.Clear()
        self.actions.Clear()
        self.emotions.Clear()
        self.model_spec.Clear()
        self.objects.Clear()
        self.image_spec.Clear()
        self.location.Clear()
        self.composition.Clear()
        self.wwwww.Clear()
        self.the_rest.Clear()
        self.search_DB.Clear()
        self.search_results.ClearAll()

    def __write_metadata_to_image(self):
        pass

    def __write_to_db(self):
        """insert actual data to database"""
        keyw_db.insert_image_data(self.__jpg_data(),
                                  self.files_list.GetString(self.files_list.GetSelection()),
                                  self.isolation.GetLineText(0),
                                  self.__get_models_str(),
                                  self.__get_property_str(),
                                  self.title.GetLineText(0),
                                  self.descr.GetLineText(0),
                                  self.concept.GetLineText(0),
                                  self.news.GetLineText(0),
                                  self.actions.GetLineText(0),
                                  self.emotions.GetLineText(0),
                                  self.model_spec.GetLineText(0),
                                  self.objects.GetLineText(0),
                                  self.image_spec.GetLineText(0),
                                  self.location.GetLineText(0),
                                  self.composition.GetLineText(0),
                                  self.wwwww.GetLineText(0),
                                  self.the_rest.GetLineText(0))

    def __jpg_data(self):
        """return bitmap as jpg binary data"""
        the_img = self.img_preview.GetBitmap().ConvertToImage()
        the_img.SetOption('quality', 50)
        the_img.SaveFile("/tmp/tmp.jpg", wx.BITMAP_TYPE_JPEG)
        the_data = open("/tmp/tmp.jpg", "rb").read()
        os.remove("/tmp/tmp.jpg")
        return the_data

    def __get_models_str(self):
        """get models list as a string"""
        return ', '.join([self.model_listbox.GetString(x) for x in self.model_listbox.GetSelections()])

    def __get_property_str(self):
        """get property owner(s) list as a string"""
        return ', '.join([self.property_listbox.GetString(x) for x in self.property_listbox.GetSelections()])

    def search_for_images_in_DB(self):
        """search for images in database and show result"""
        self.search_results.ClearAll()
        self.image_list.RemoveAll()
        search_str = self.search_DB.GetLineText(0)
        if len(search_str) > 0:
            # print(" search for images in DB with string:", search_str)
            results = keyw_db.get_search_data(search_str)
            # print(f"got {len(results)} results")
            if len(results) > 0:
                the_index = 0
                for result in results:
                    the_image = wx.Image(io.BytesIO(result[0]), type=wx.BITMAP_TYPE_JPEG)
                    w, h = the_image.GetSize()
                    if w < 256:
                        dx = round((256 - w)/2)
                        dy = 0
                    else:
                        dx = 0
                        dy = round((256 - h)/2)
                    self.image_list.Add(wx.Bitmap(the_image.Resize((256, 256), (dx, dy), red=-1, green=-1, blue=-1)))
                    self.search_results.InsertItem(the_index, result[1], the_index)
                    the_index += 1

    def populate_text_fields_using_search_results(self):
        if self.search_results.GetSelectedItemCount() > 0:
            selected_files = []
            item = self.search_results.GetFirstSelected()
            while item != -1:
                data = self.search_results.GetItem(item)
                selected_files.append(data.Text)
                item = self.search_results.GetNextSelected(item)

            imgs_data = keyw_db.get_imgs_data(selected_files)
            if len(imgs_data[6]) > 0:
                self.concept.AppendText(imgs_data[6])
            if len(imgs_data[7]) > 0:
                self.news.AppendText(imgs_data[7])
            if len(imgs_data[8]) > 0:
                self.actions.AppendText(imgs_data[8])
            if len(imgs_data[9]) > 0:
                self.emotions.AppendText(imgs_data[9])
            if len(imgs_data[10]) > 0:
                self.model_spec.AppendText(imgs_data[10])
            if len(imgs_data[11]) > 0:
                self.objects.AppendText(imgs_data[11])
            if len(imgs_data[12]) > 0:
                self.image_spec.AppendText(imgs_data[12])
            if len(imgs_data[13]) > 0:
                self.location.AppendText(imgs_data[13])
            if len(imgs_data[14]) > 0:
                self.composition.AppendText(imgs_data[14])
            if len(imgs_data[15]) > 0:
                self.wwwww.AppendText(imgs_data[15])
            if len(imgs_data[16]) > 0:
                self.the_rest.AppendText(imgs_data[16])

            self.main_notebook.ChangeSelection(0)





