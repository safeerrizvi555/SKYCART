"""
=============================================================================
ADVANCED E-COMMERCE ROUTING ENGINE (PRODUCTION READY)
=============================================================================
Description: Ye main application file hai jo user ki navigation ko control karti hai.
Is mein koi Signup ya Login system nahi hai. Ye directly products aur categories
ko serve karne ke liye banai gayi hai.

Flow:
1. '/' -> introduction.html (Entry point)
2. '/dashboard' -> dashboard.html (Category Selection)
3. '/men', '/women', '/kids' -> Specific Product Pages
=============================================================================
"""

from flask import Flask, render_template, request, make_response, redirect, url_for
import os
import time

# ---------------------------------------------------------------------------
# 1. APPLICATION SETUP & CONFIGURATION
# ---------------------------------------------------------------------------
# Flask app ko initialize kar rahe hain aur static/templates folder link kar rahe hain
app = Flask(__name__, static_folder="static", template_folder="templates")


# Advanced Configurations (Pro-Level)
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secure-key-2026")
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max upload limit
    TEMPLATES_AUTO_RELOAD = True  # Templates automatically reload honge
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # Static files caching (1 year)


app.config.from_object(Config)


# ---------------------------------------------------------------------------
# 2. SECURITY & HEADERS MIDDLEWARE
# ---------------------------------------------------------------------------
# Ye section website ko secure banata hai. Ye pro developers use karte hain
# taake unki website hack na ho sake aur fast load ho.
@app.after_request
def apply_caching_and_security(response):
    """Har page load hone ke baad ye function run hoga aur security add karega."""
    # XSS aur Clickjacking se bachne ke headers
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # Agar static file (image/css) hai to usay cache kar lo taake website fast ho
    if request.endpoint == "static":
        response.headers["Cache-Control"] = "public, max-age=31536000"
    else:
        # HTML pages ko cache mat karo taake hamesha fresh update mile
        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, max-age=0"
        )

    return response


# ---------------------------------------------------------------------------
# 3. GLOBAL CONTEXT PROCESSOR
# ---------------------------------------------------------------------------
# Ye function automatically har HTML page ko kuch basic data bhejta hai,
# aap ko bar bar variables define nahi karne parte.
@app.context_processor
def inject_global_variables():
    return {
        "project_version": "1.0",
        "current_year": time.strftime("%Y"),
        "site_name": "SkyCart Elite",
    }


# ---------------------------------------------------------------------------
# 4. CORE PAGE ROUTING (USER NAVIGATION FLOW)
# ---------------------------------------------------------------------------


@app.route("/", methods=["GET"])
def introduction():
    """
    STEP 1: Introduction Page.
    Jab user website open karega to sab se pehle ye page aayega.
    Is page par ek 'Next' button hoga jo user ko dashboard par le jayega.
    """
    return render_template("introduction.html")


@app.route("/dashboard", methods=["GET"])
def dashboard():
    """
    STEP 2: Main Dashboard.
    Introduction page se user yahan aayega. Ye website ka dil hai jahan se
    user decide karega ke usay Men, Women, ya Kids section mein jana hai.
    """
    return render_template("dashboard.html")


# ---------------------------------------------------------------------------
# 5. CATEGORY ROUTING (MEN, WOMEN, KIDS)
# ---------------------------------------------------------------------------


@app.route("/men", methods=["GET"])
def men_section():
    """
    STEP 3A: Men's Collection.
    Agar user dashboard se 'Men' select karta hai, to ye page open hoga
    aur m1.webp, m2.webp jaisi images show karega.
    """
    return render_template("men.html")


@app.route("/women", methods=["GET"])
def women_section():
    """
    STEP 3B: Women's Collection.
    Agar user dashboard se 'Women' select karta hai, to ye page open hoga
    aur w1.jpg, w2.webp jaisi images display hongi.
    """
    return render_template("women.html")


@app.route("/kids", methods=["GET"])
def kids_section():
    """
    STEP 3C: Kids' Collection.
    Agar user dashboard se 'Kids' select karta hai, to ye page open hoga
    aur k1.jpg, k2.jpg products load karega.
    """
    return render_template("kids.html")


# ---------------------------------------------------------------------------
# 6. ADVANCED ERROR HANDLING
# ---------------------------------------------------------------------------
# Agar user galti se koi aisa URL type kar de jo exist nahi karta,
# to website crash nahi hogi, balkay ek khubsurat error page aayega.


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 - Page Not Found Errors"""
    # Aap ki banayi hui error.html file load hogi
    return (
        render_template(
            "error.html",
            error_title="404 - Not Found",
            error_message="Aap jo page dhoond rahe hain wo majood nahi hai.",
        ),
        404,
    )


@app.errorhandler(500)
def server_error(e):
    """Handle 500 - Internal Server Errors"""
    return (
        render_template(
            "error.html",
            error_title="500 - Server Error",
            error_message="Server mein koi masla aa gaya hai. Please thori der baad try karein.",
        ),
        500,
    )


@app.errorhandler(403)
def forbidden_error(e):
    """Handle 403 - Forbidden Access"""
    return (
        render_template(
            "error.html",
            error_title="403 - Access Denied",
            error_message="Aap ko is page par jane ki ijazat nahi hai.",
        ),
        403,
    )


# ---------------------------------------------------------------------------
# 7. SERVER EXECUTION
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Server run karne ki command. Debug True rakha gaya hai taake aap
    # asani se files edit kar sakein aur changes foran show hon.
    print("[SYSTEM] Starting Advanced Routing Engine...")
    print("[SYSTEM] Access the website at: http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
  
