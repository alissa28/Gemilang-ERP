import os
from flask import Blueprint, render_template, send_from_directory
from flask_cors import cross_origin
from app.utils.session_validation import session_required
from app.utils.auth_utils import privilege_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
@privilege_required('view_reports')
@session_required
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/inventory/input')
@privilege_required('view_reports')
@session_required 
def stock_input():
    return render_template('inputbarang.html')

@main_bp.route('/inventory/history')
@privilege_required('view_reports')
@session_required
def stock_history():
    return render_template('historybarang.html')

@main_bp.route('/operational')
@session_required
def operational_main():
    return render_template('pos.html')

@main_bp.route('/purchase')
@session_required
def purchase_main():
    return render_template('purchase.html')

@main_bp.route('/sale')
@session_required
def sale_main():
    return render_template('pos.html')

@main_bp.route('/sale_report')
@privilege_required('view_reports')
@session_required
def sale_report():
    return render_template('sale_report.html')

@main_bp.route('/modul_panduan')
@session_required
def modul_panduan():
    pdf_path = os.path.join('static', 'media', 'pdf')
    return send_from_directory(pdf_path, 'Modul Panduan SIstem ERP Toko Gemilang (2).pdf')

