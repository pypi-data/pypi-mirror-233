from django.conf import settings


class _DefaultSettings:
    CJKCMS_FONT_URL = "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"  # noqa

    CJKCMS_FONT_FAMILY = "Roboto, sans-serif"

    CJKCMS_BRAND_LOGO_LONG = "cjkcms/images/logos/cms-logo-long.svg"
    CJKCMS_BRAND_LOGO_SQUARE = "cjkcms/images/logos/cms-logo-square.svg"
    CJKCMS_FRONTEND_BTN_SIZE_DEFAULT = ""
    CJKCMS_FRONTEND_BTN_SIZE_CHOICES = [
        ("btn-sm", "Small"),
        ("", "Default"),
        ("btn-lg", "Large"),
    ]

    CJKCMS_FRONTEND_BTN_STYLE_DEFAULT = "btn-primary"
    CJKCMS_FRONTEND_BTN_STYLE_CHOICES = [
        ("btn-primary", "Primary"),
        ("btn-secondary", "Secondary"),
        ("btn-success", "Success"),
        ("btn-danger", "Danger"),
        ("btn-warning", "Warning"),
        ("btn-info", "Info"),
        ("btn-link", "Link"),
        ("btn-light", "Light"),
        ("btn-dark", "Dark"),
        ("btn-outline-primary", "Outline Primary"),
        ("btn-outline-secondary", "Outline Secondary"),
        ("btn-outline-success", "Outline Success"),
        ("btn-outline-danger", "Outline Danger"),
        ("btn-outline-warning", "Outline Warning"),
        ("btn-outline-info", "Outline Info"),
        ("btn-outline-light", "Outline Light"),
        ("btn-outline-dark", "Outline Dark"),
    ]

    CJKCMS_FRONTEND_CAROUSEL_FX_DEFAULT = ""
    CJKCMS_FRONTEND_CAROUSEL_FX_CHOICES = [
        ("", "Slide"),
        ("carousel-fade", "Fade"),
    ]

    CJKCMS_FRONTEND_COL_SIZE_DEFAULT = ""
    CJKCMS_FRONTEND_COL_SIZE_CHOICES = [
        ("", "Automatically size"),
        ("12", "Full row"),
        ("6", "Half - 1/2 column"),
        ("4", "Thirds - 1/3 column"),
        ("8", "Thirds - 2/3 column"),
        ("3", "Quarters - 1/4 column"),
        ("9", "Quarters - 3/4 column"),
        ("2", "Sixths - 1/6 column"),
        ("10", "Sixths - 5/6 column"),
        ("1", "Twelfths - 1/12 column"),
        ("5", "Twelfths - 5/12 column"),
        ("7", "Twelfths - 7/12 column"),
        ("11", "Twelfths - 11/12 column"),
    ]

    CJKCMS_FRONTEND_COL_BREAK_DEFAULT = "md"
    CJKCMS_FRONTEND_COL_BREAK_CHOICES = [
        ("", "Always expanded"),
        ("sm", "sm - Expand on small screens (phone, 576px) and larger"),
        ("md", "md - Expand on medium screens (tablet, 768px) and larger"),
        ("lg", "lg - Expand on large screens (laptop, 992px) and larger"),
        ("xl", "xl - Expand on extra large screens (wide monitor, 1200px)"),
    ]

    CJKCMS_FRONTEND_NAVBAR_FORMAT_DEFAULT = ""
    CJKCMS_FRONTEND_NAVBAR_FORMAT_CHOICES = [
        ("", "Default Bootstrap Navbar"),
        ("cjkcms-navbar-center", "Centered logo at top"),
    ]

    CJKCMS_LANGUAGE_SELECTOR_DEFAULT = None
    CJKCMS_LANGUAGE_SELECTOR_CHOICES = [
        (None, "None"),
        ("cjkcms/snippets/navbar_lang_selector.html", "Menu Dropdown Selector"),
        ("cjkcms/snippets/bottom_corner_lang_selector.html", "Bottom Corner Selector"),
    ]

    CJKCMS_FRONTEND_NAVBAR_COLOR_SCHEME_DEFAULT = "navbar-light"
    CJKCMS_FRONTEND_NAVBAR_COLOR_SCHEME_CHOICES = [
        ("navbar-light", "Light - for use with a light-colored navbar"),
        ("navbar-dark", "Dark - for use with a dark-colored navbar"),
    ]

    CJKCMS_FRONTEND_NAVBAR_CLASS_DEFAULT = "bg-light"

    CJKCMS_FRONTEND_NAVBAR_COLLAPSE_MODE_DEFAULT = "navbar-expand-lg"
    CJKCMS_FRONTEND_NAVBAR_COLLAPSE_MODE_CHOICES = [
        ("", "Never show menu - Always collapse menu behind a button"),
        ("navbar-expand-sm", "sm - Show on small screens (phone size) and larger"),
        ("navbar-expand-md", "md - Show on medium screens (tablet size) and larger"),
        ("navbar-expand-lg", "lg - Show on large screens (laptop size) and larger"),
        (
            "navbar-expand-xl",
            "xl - Show on extra large screens (desktop, wide monitor)",
        ),
    ]

    CJKCMS_FRONTENT_NAVBAR_SEARCHBOX_CLASS = "border-secondary mb-0"
    CJKCMS_FRONTEND_THEME_HELP = "Change the source of your Bootstrap theme."
    CJKCMS_FRONTEND_THEME_DEFAULT = ""
    CJKCMS_FRONTEND_THEME_CHOICES = (
        ("", "Default - Built-in Bootstrap 5"),
        ("mdb.light", "Built-in MDBootstrap 5"),
        ("mdb.dark", "Built-in MDBootstrap 5 dark"),
        ("python-webpack", "Python Webpack Boilerplate by Michael Yin"),
    )

    CJKCMS_FRONTEND_TEMPLATES_BLOCKS = {
        "cardblock": [
            ("cjkcms/blocks/card_block.html", "Card"),
            ("cjkcms/blocks/card_horizontal.html", "Horizontal Card"),
            ("cjkcms/blocks/card_horizontal2.html", "Horizontal with background fill"),
            ("cjkcms/blocks/card_head.html", "Card with header"),
            ("cjkcms/blocks/card_foot.html", "Card with footer"),
            ("cjkcms/blocks/card_head_foot.html", "Card with header and footer"),
            ("cjkcms/blocks/card_blurb.html", "Blurb - rounded image and no border"),
            ("cjkcms/blocks/card_img.html", "Cover image - use image as background"),
            ("cjkcms/blocks/card_landing1.html", "Landing page style 1"),
            ("cjkcms/blocks/card_landing2.html", "Landing page style 2"),
        ],
        "cardgridblock": [
            (
                "cjkcms/blocks/cardgrid_group.html",
                "Card group - attached cards of equal size",
            ),
            (
                "cjkcms/blocks/cardgrid_deck.html",
                "Card deck - separate cards of equal size",
            ),
            (
                "cjkcms/blocks/cardgrid_columns.html",
                "Card masonry - fluid brick pattern",
            ),
        ],
        # DEPRECATED
        "pagelistblock": [
            ("cjkcms/blocks/pagelist_block.html", "General, simple list"),
            (
                "cjkcms/blocks/pagelist_list_group.html",
                "General, list group navigation panel",
            ),
            (
                "cjkcms/blocks/pagelist_toc_nextprev.html",
                "TOC navigation with prev / next",
            ),
            ("cjkcms/blocks/pagelist_article_media.html", "Article, media format"),
            (
                "cjkcms/blocks/pagelist_article_card_group.html",
                "Article, card group - attached cards of equal size",
            ),
            (
                "cjkcms/blocks/pagelist_article_card_deck.html",
                "Article, card deck - separate cards of equal size",
            ),
            (
                "cjkcms/blocks/pagelist_article_card_columns.html",
                "Article, card masonry - fluid brick pattern",
            ),
        ],
        # DEPRECATED
        "pagepreviewblock": [
            ("cjkcms/blocks/pagepreview_card.html", "Card"),
        ],
        "quoteblock": [
            ("cjkcms/blocks/quote_block.html", "Simple blockquote"),
            ("cjkcms/blocks/quote_block_leftbar.html", "Quote with left bar"),
            ("cjkcms/blocks/quote_block_start_end_quote.html", "With start/end quote"),
        ],
        # templates that are available for all block types
        "*": [
            ("", "Default"),
        ],
    }

    CJKCMS_FRONTEND_TEMPLATES_PAGES = {
        # templates that are available for all page types
        "*": [
            ("", "Default"),
            ("cjkcms/pages/web_page.html", "Web page showing title and cover image"),
            (
                "cjkcms/pages/web_page_notitle.html",
                "Web page without title and cover image",
            ),
            ("cjkcms/pages/base.html", "Blank page - no navbar or footer"),
        ],
    }

    CJKCMS_BANNER = None
    CJKCMS_BANNER_BACKGROUND = "#f00"
    CJKCMS_BANNER_TEXT_COLOR = "#fff"

    CJKCMS_BASE_TEMPLATE_HELP = (
        "Base template used by CMS pages, defaults to CMS built-in one"
    )
    CJKCMS_BASE_TEMPLATE_DEFAULT = "cjkcms/pages/base.html"
    CJKCMS_AUTH_VISIBILITY_DEFAULT = "all"
    CJKCMS_AUTH_VISIBILITY_CHOICES = (
        ("all", "Default (Everyone)"),
        ("non-auth-only", "Not logged in only"),
        ("auth-only", "Logged in only"),
        ("include-groups", "Visible for selected groups"),
        ("exclude-groups", "Hidden for selected groups"),
        ("hidden", "Hidden for all"),
    )

    BANNER = None
    BANNER_BACKGROUND = "#f00"
    BANNER_TEXT_COLOR = "#fff"

    CJKCMS_RICHTEXT_FEATURES = {
        "default": [
            "h2",
            "h3",
            "h4",
            "bold",
            "italic",
            "link",
            "ol",
            "ul",
            "hr",
            "blockquote",
            "image",
            "centre-align",
            "left-align",
            "right-align",
        ],
        "full": [
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "bold",
            "italic",
            "underline",
            "ol",
            "ul",
            "larger",
            "smaller",
            "superscript",
            "subscript",
            "strikethrough",
            "link",
            "hr",
            "code",
            "document-link",
            "blockquote",
            "image",
            "embed",
            "centre-align",
            "left-align",
            "right-align",
        ],
        "minimal": ["bold", "italic", "link"],
    }

    CJKCMS_SOC_MEDIA_TEMPLATE = "cjkcms/snippets/social_media.html"
    CJKCMS_SOC_LOCATION_DEFAULT = "none"
    CJKCMS_SOC_LOCATION_CHOICES = [
        ("left", "left"),
        ("right", "right"),
        ("menu", "menu"),
        ("none", "none"),
    ]

    CJKCMS_BUTTON_SIZE_DEFAULT = "btn-sm"
    CJKCMS_BUTTON_SIZE_CHOICES = [
        ("btn-sm", "Small"),
        ("btn-md", "Medium"),
        ("btn-lg", "Large"),
    ]

    CJKCMS_BUTTON_COLOR_DEFAULT = "btn-primary"
    CJKCMS_BUTTON_COLOR_CHOICES = [
        ("btn-primary", "Primary"),
        ("btn-outline-primary", "Primary Outline"),
        ("btn-secondary", "Secondary"),
        ("btn-outline-secondary", "Secondary Outline"),
        ("btn-success", "Success"),
        ("btn-outline-success", "Success Outline"),
        ("btn-danger", "Danger"),
        ("btn-outline-danger", "Danger Outline"),
        ("btn-warning", "Warning"),
        ("btn-outline-warning", "Warning Outline"),
        ("btn-info", "Info"),
        ("btn-outline-info", "Info Outline"),
        ("btn-light", "Light"),
        ("btn-outline-light", "Light Outline"),
        ("btn-dark", "Dark"),
        ("btn-outline-dark", "Dark Outline"),
        ("btn-link", "Link"),
        ("btn-outline-link", "Link Outline"),
    ]

    def __getattribute__(self, attr: str):
        # First load from Django settings.
        # If it does not exist, load from _DefaultSettings.
        try:
            return getattr(settings, attr)
        except AttributeError:
            return super().__getattribute__(attr)


cms_settings = _DefaultSettings()
