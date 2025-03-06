class Config:
    # Style
    roughness = font_family = code_font_family = 0
    # Theme
    background_color = ""
    text_color = ""
    out_text_color = ""
    title_text_color = ""
    container_title_text_color = ""
    arrow_color = ""
    container_background = ""
    command_background_color = ""
    info_background_color = ""
    border_color = ""
    main_title_border_color = ""
    cve_color = ""
    cve_text_color = ""

    # main title
    main_title_width = 1300
    main_image_width = 386
    main_image_height = 73
    main_title_height = main_image_height + 20 + 20
    main_title_line_width = 4
    main_title_line = "dashed"  # "solid"
    main_title_roughness = None
    main_title_font_family = None
    main_title_font_size = 50

    # global
    space_height = 30
    space_width = 50

    # title
    title_height = 50
    title_width = 400
    title_font_size = 20
    title_new_line_nb_chars = 35

    # command
    command_font_family = None
    command_height = 50
    command_width = 300
    command_line_width = 2
    command_roughness = None
    command_new_line_nb_chars = 65

    # info
    info_font_family = None
    info_height = 50
    info_width = 150
    info_line_width = 2
    info_roughness = None
    info_new_line_nb_chars = 35

    # cve_style

    # container
    container_title_width = 500
    container_title_height = 50
    container_line = "dashed"  # "solid"
    container_line_width = 4
    container_new_line_nb_chars = 40

    # container padding
    padding_width = 50
    padding_height = 30

    # title -> command arrow
    title_command_arrow_end = None  # "triangle"
    title_roughness = None

    # image
    image_width = 44
    image_height = 44
    icon_path = './icon'

    # out
    out_line_width = 30
    out_space_width = 20
    out_space_height = 10
    out_width = 200
    out_height = 50
    out_line_line_width = 2
    out_font_family = None
    default_out_color = "#c3c6c9"
    out_roughness = None
    out_new_line_nb_chars = 20

    @classmethod
    def set_style(cls, style):
        if style == 'handraw':
            # style hand draw
            cls.roughness = 2   # 0: architect / 1:artist / 2: handdraw
            cls.font_family = 5 # 6: normal / 5: handraw / 8: code
            cls.code_font_family = 8
        else:
            # style clean (default)
            cls.roughness = 0  # 0: architect / 1:artist / 2: handdraw
            cls.font_family = 6  # 6: normal / 5: handraw / 8: code
            cls.code_font_family = 6

    @classmethod
    def set_theme(cls, theme):
        if theme == 'light':
            # white theme
            cls.background_color = "#fff"
            cls.text_color = "#1e1e1e"
            cls.out_text_color = "#1e1e1e"
            cls.title_text_color = "#1e1e1e"
            cls.container_title_text_color = "#1e1e1e"
            cls.container_background = "#e9ecef"
            cls.arrow_color = "#1e1e1e"
            cls.command_background_color = "#f8f1ee"
            cls.info_background_color = "#f8f1ee"
            cls.border_color = "#1e1e1e"
            cls.main_title_border_color = "#1e1e1e"
            cls.cve_color = "#FAD7AC" #"#ffc9c9"
            cls.cve_text_color = "#1e1e1e"
        else:
            # dark theme (default)
            cls.background_color = "#000"
            cls.text_color = "#fff"
            cls.out_text_color = "#1e1e1e"
            cls.title_text_color = "#1e1e1e"
            cls.container_title_text_color = "#1e1e1e"
            cls.arrow_color = "#fff"
            cls.container_background = "#2b2f32"
            cls.command_background_color = "#1f1f1f"
            cls.info_background_color = "#333"
            cls.border_color = "#868e96"
            cls.main_title_border_color = "#868e96"
            cls.cve_color = "#FAD7AC"
            cls.cve_text_color = "#1e1e1e"
        cls.apply_theme()

    @classmethod
    def apply_theme(cls):
        # main title
        cls.main_title_roughness = cls.roughness
        cls.main_title_font_family = cls.font_family
        # command
        cls.command_font_family = cls.code_font_family
        cls.command_roughness = cls.roughness

        # info
        cls.info_font_family = cls.font_family
        cls.info_roughness = cls.roughness
        # title -> command arrow
        cls.title_roughness = cls.roughness
        # out
        cls.out_font_family = cls.font_family
        cls.out_roughness = cls.roughness