
def generate_html_divider(label_text):
    divider = '<div style="text-align:center;">'
    divider += '<hr style="height: 3px; border: none; background-color: #f2f2f2; margin: 25px 0;" />'
    divider += f'<span style="display:inline-block; position:relative; top:-1.5em; padding: 0 20px; background-color:#fff; font-size: 1.2em; font-weight:bold; color: #555; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); border-radius: 5px; font-family: Arial, sans-serif; letter-spacing: 2px;">{label_text}</span>'
    divider += '</div>'
    return divider


def generate_title_banner(title_text, color_theme="2a4b71"):
    banner_html = f"""
    <div class="banner-container">
        <div class="banner-text">{title_text}</div>
    </div>
    <div class="menu-bar">
        <a href="https://nijitracker.com/">Nijitracker</a>
        <a href="https://nijitracker.com/pettantracker">PettanTracker</a>
    </div>
    <style>
        .banner-container {{
            background-color: #{color_theme};
            color: white;
            text-align: center;
            font-size: 6em;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: bold;
            padding: 0.2em 0;
            margin-bottom: 0.5em;
            margin: 0;
            position: relative;
            word-wrap: break-word;
        }}
        .banner-text {{
            animation-name: slideInDown;
            animation-duration: 1s;
            animation-timing-function: ease;
            animation-delay: 0s;
            animation-fill-mode: both;
        }}
        .menu-bar {{
            background-color: #f2f2f2;
            overflow: hidden;
            position: relative;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 1.5em;
            font-weight: bold;
            text-align: center;
        }}
        .menu-bar a {{
            display: inline-block;
            color: #{color_theme};
            text-align: center;
            padding: 14px 16px;
            text-decoration: none;
            transition: 0.3s;
        }}
        .menu-bar a:hover {{
            background-color: #{color_theme};
            color: white;
        }}
        @keyframes slideInDown {{
            0% {{
                transform: translateY(-100%);
                opacity: 0;
            }}
            100% {{
                transform: translateY(0);
                opacity: 1;
            }}
        }}
        @media (max-width: 768px) {{
            .banner-container {{
                font-size: 3em;
                padding: 0.2em 0.5em;
            }}
            .menu-bar a {{
                font-size: 1em;
            }}
        }}
        @media (max-width: 480px) {{
            .banner-container {{
                font-size: 2em;
                padding: 0.2em 0.5em;
            }}
            .menu-bar a {{
                font-size: 0.8em;
            }}
        }}
    </style>
    """
    return banner_html




def generate_meta_data(title: str, description: str, image_url: str):
    return f"""<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8"/>
    <head>
    <title>{title}</title>
    <link rel="icon" type="image/x-icon" href="{image_url}">
    <meta name="description" content="{description}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Google / Search Engine Tags -->
    <meta itemprop="name" content="{title}">
    <meta itemprop="description" content="{description}">
    <meta itemprop="image" content="{image_url}">

    <!-- Facebook Meta Tags -->
    <meta property="og:url" content="http://nijitracker.com">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{image_url}">

    <!-- Twitter Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{image_url}">
    </head>
    <body>
    """

def build_footer_info(info: str):
    footer = f"""
        <div style='background-color: #f5f5f5; padding: 20px; font-size: 16px; font-family: "Open Sans", sans-serif;'>
            <div style='text-align: center;'>
                <span style='font-weight: bold;'>Information</span>
            </div>
            <div style='margin-top: 20px; 'text-align': center'>
                <p style='text-align: center;'>Data for this site is taken every hour. Due to limitation with YouTube's API only certain increments in subscriber counts will be reflected based on each liver's channel size</p>
                <p style='text-align: center;'>Each liver has their own page to track their own individual achievements and subscriber count. The full table of all recorded daily data for each channel is also viewable</p>
            </div>
            <div style='text-align: center;'>
                <span style='font-weight: bold;'>A Note on Graduating Livers</span>
            </div>
            <div style='margin-top: 20px; 'text-align': center'>
                <p style='text-align: center;'>If a liver is determined to be graduating, retiring, or terminated, Nijitracker will stop tracking their subscriber count, and their page and entry will be removed</p>
                <p style='text-align: center;'>Historical data is still retrievable through the Nijitracker API <a href="http://api.nijitracker.com">api.nijitracker.com</a>
                </p>         
            </div>
            <div style='margin-top: 20px; 'text-align': center'>
                <p style='text-align: center;'>{info}</p>
            </div>
            <div style='text-align: center; margin-top: 20px;'>
                <a href='https://github.com/pinapelz/NijiTrack' target='_blank'>
                    <img src='https://img.shields.io/github/license/pinapelz/NijiTrack?color=%23994CC3&style=flat-square' alt='License'/>
                </a>
            </div>
        </div>
    """
    return footer

def side_swipe_header(text: str, color_theme="007ACC", url: str="https://nijitracker.com"):
    banner_html = f"""
    <a href="{url}" target="_self" rel="noopener noreferrer">
        <div class="banner-container">
            <div class="banner-text">{text}</div>
        </div>
    </a>
    <style>
        .banner-container {{
            background-color: #{color_theme};
            color: white;
            text-align: center;
            font-size: 6em;
            font-family: 'Montserrat', sans-serif;
            font-weight: bold;
            padding: 0.2em 0;
            margin-bottom: 0.5em;
            margin: 0;
            position: relative;
        }}
        
        .banner-text {{
            position: relative;
            animation-name: slideInRight;
            animation-duration: 1s;
            animation-timing-function: ease;
            animation-delay: 0s;
            animation-fill-mode: both;
        }}
        
        @keyframes slideInRight {{
            0% {{
                transform: translateX(-100%);
                opacity: 0;
            }}
            100% {{
                transform: translateX(0);
                opacity: 1;
            }}
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            .banner-container {{
                font-size: 4em;
            }}
        }}
        
        @media (max-width: 576px) {{
            .banner-container {{
                font-size: 3em;
            }}
        }}
    </style>
    """
    return banner_html



def generate_info_card(name, youtube_channel_id, profile_pic, description):
    # Build the HTML string
    html = f"""
    <br>
    <style>
        .info-card {{
            display: flex;
            flex-direction: row;
            align-items: center;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            overflow: hidden;
        }}

        .img-wrapper {{
            width: 200px;
            height: 200px;
            overflow: hidden;
        }}

        .img-wrapper img {{
            width: 100%;
            height: auto;
        }}

        .text-wrapper {{
            flex: 1;
            padding: 20px;
        }}

        h2 {{
            font-size: 24px;
            margin-bottom: 10px;
            font-family: Arial, sans-serif;
        }}

        p {{
            font-size: 16px;
            margin-bottom: 20px;
            font-family: Arial, sans-serif;
        }}
        a{{
            font-family: Arial, sans-serif;
        }}

        .button {{
            display: inline-block;
            padding: 10px 20px;
            border-radius: 20px;
            background-color: #0077b5;
            color: #fff;
            text-decoration: none;
            transition: background-color 0.2s ease;
        }}

        .button:hover {{
            background-color: #005ea3;
        }}
        
        @media only screen and (max-width: 768px) {{
            .info-card {{
                flex-direction: column;
                align-items: flex-start;
            }}
            .img-wrapper {{
                width: 100%;
                height: 250px;
                margin-bottom: 20px;
            }}
            .text-wrapper {{
                width: 100%;
                white-space: pre-line;
            }}
        }}
    </style>
    <div class="info-card">
        <div class="img-wrapper">
            <img src="{profile_pic}" alt="{name}">
        </div>
        <div class="text-wrapper">
            <h2>{name}</h2>
            <p>{description}</p>
            <a class="button" href="https://www.youtube.com/channel/{youtube_channel_id}">YouTube Channel</a>
        </div>
    </div>
    """
    # Return the HTML string
    return html


def generate_subscriber_info_card(subscriber_count):
    formatted_sub_count = "{:,.0f}".format(int(subscriber_count))
    html_template = f'''
    <div style="display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #F7FAFC;">
        <div style="background-color: #ffffff; border-radius: 10px; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);">
            <h2 style="font-family: 'Helvetica Neue', sans-serif; font-size: 72px; font-weight: bold; margin-bottom: 10px; text-align: center;">{formatted_sub_count}</h2>
            <p style="font-family: 'Helvetica Neue', sans-serif; font-size: 24px; margin-bottom: 0; text-align: center;">Subscribers</p>
        </div>
    </div>
    '''
    return html_template

def generate_full_table_button(url):
    button_html = """
    <style>
        .btn {
            display: inline-block;
            font-weight: 400;
            text-align: center;
            white-space: nowrap;
            vertical-align: middle;
            user-select: none;
            border: 1px solid transparent;
            padding: .375rem .75rem;
            font-size: 1rem;
            line-height: 1.5;
            border-radius: .25rem;
            transition: color .15s ease-in-out,
                        background-color .15s ease-in-out,
                        border-color .15s ease-in-out,
                        box-shadow .15s ease-in-out;
            color: #fff;
            background-color: #007bff;
            border-color: #007bff;
            margin: 0 auto;
            display: block;
            max-width: 200px;
        }

        .btn:hover {
            color: #fff;
            background-color: #0069d9;
            border-color: #0062cc;
        }

        .btn:focus, .btn.focus {
            outline: 0;
            box-shadow: 0 0 0 .2rem rgba(0, 123, 255, .5);
        }

        .btn-lg {
            font-size: 1.25rem;
            line-height: 1.5;
            padding: .3rem .75rem;
            border-radius: .3rem;
        }
    </style>
    <br>

    """
    button_html += f"""<a href="{url}" class="btn btn-primary btn-lg" role="button">View Full Table</a>"""
    return button_html

def generate_doctype_footer():
    return """
    </body>
    </html>
    """