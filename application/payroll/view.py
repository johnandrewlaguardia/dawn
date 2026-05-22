from flask import Blueprint, render_template, request, redirect, url_for, flash

from application.extension import db
from application.payroll.models import Payroll
from application.user.models import User

bp = Blueprint(
    'payroll',
    __name__,
    url_prefix='/payroll'
)


@bp.route('/')
def index():

    payrolls = Payroll.query.order_by(Payroll.created_at.desc()).all()

    return render_template(
        'payroll/index.html',
        payrolls=payrolls
    )


@bp.route('/report')
def report():
    """Payroll report view - shows all payrolls in a printable format"""

    payrolls = Payroll.query.order_by(Payroll.payroll_period.desc(), Payroll.user_id).all()

    return render_template(
        'payroll/report.html',
        payrolls=payrolls
    )


@bp.route('/generate', methods=['GET', 'POST'])
def generate():
    """Generate payroll for active employees for a specific period"""

    if request.method == 'POST':

        payroll_period = request.form['payroll_period']

        # Get all active employees
        active_employees = User.query.filter_by(is_active=True).all()

        if not active_employees:
            flash('No active employees found', 'warning')
            return redirect(url_for('payroll.generate'))

        try:
            # Create payroll records for all active employees
            for employee in active_employees:
                # Check if payroll already exists for this period
                existing = Payroll.query.filter_by(
                    user_id=employee.id,
                    payroll_period=payroll_period
                ).first()

                if not existing:
                    payroll = Payroll(
                        allowance=0,
                        deduction=0,
                        overtime=0,
                        payroll_date=payroll_period,
                        payroll_period=payroll_period,
                        salary_snapshot=employee.basic_salary,
                        employee_name=employee.username,
                        net_pay=employee.basic_salary,
                        user_id=employee.id
                    )
                    db.session.add(payroll)

            db.session.commit()
            flash(f'Payroll generated for {len(active_employees)} active employees for period {payroll_period}', 'success')
            return redirect(url_for('payroll.index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error generating payroll: {str(e)}', 'danger')
            return redirect(url_for('payroll.generate'))

    return render_template(
        'payroll/generate.html'
    )


@bp.route('/create', methods=['GET', 'POST'])
def create():

    users = User.query.filter_by(is_active=True).all()

    if request.method == 'POST':

        user_id = request.form['user_id']

        allowance = float(request.form['allowance'])
        deduction = float(request.form['deduction'])
        overtime = float(request.form['overtime'])

        payroll_date = request.form['payroll_date']
        payroll_period = request.form.get('payroll_period', payroll_date)

        user = User.query.get(user_id)

        net_pay = (
            user.basic_salary
            + allowance
            + overtime
            - deduction
        )

        payroll = Payroll(
            allowance=allowance,
            deduction=deduction,
            overtime=overtime,
            salary_snapshot=user.basic_salary,
            employee_name=user.username,
            payroll_date=payroll_date,
            payroll_period=payroll_period,
            net_pay=net_pay,
            user_id=user_id
        )

        db.session.add(payroll)
        db.session.commit()

        return redirect(url_for('payroll.index'))

    return render_template(
        'payroll/create.html',
        users=users
    )


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):

    payroll = Payroll.query.get_or_404(id)

    if request.method == 'POST':

        allowance = float(request.form['allowance'])
        deduction = float(request.form['deduction'])
        overtime = float(request.form['overtime'])
        payroll_date = request.form['payroll_date']
        payroll_period = request.form.get('payroll_period', payroll.payroll_period)

        payroll.allowance = allowance
        payroll.deduction = deduction
        payroll.overtime = overtime
        payroll.payroll_date = payroll_date
        payroll.payroll_period = payroll_period
        payroll.net_pay = (
            payroll.salary_snapshot
            + allowance
            + overtime
            - deduction
        )

        db.session.commit()

        return redirect(url_for('payroll.index'))

    return render_template(
        'payroll/edit.html',
        payroll=payroll
    )