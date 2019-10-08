from flask import render_template, flash, redirect, url_for
from app import app
from flask_login import current_user, login_user
from app.models import UserBasic
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app.wallet import bp
from app import db
from app.wallet.forms import NewTransactionForm
from app.models import Mission, Transaction
from datetime import datetime
from sqlalchemy import func

@bp.route('/my_wallet', methods=['GET', 'POST'])
@login_required
def my_wallet():
    form = NewTransactionForm()
    if form.validate_on_submit():
        t = Transaction(transaction_type=form.transaction_type.data, value=form.value.data, user=current_user)
        db.session.add(t)
        db.session.commit()
        flash('New transaction updated!')
        return redirect(url_for('wallet.my_wallet'))

    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    current_sum = db.session.query(func.sum(Transaction.value)).filter_by(user_id=current_user.id).scalar()
    if current_sum is None:
        current_sum = 0
    return render_template("wallet/my_wallet.html", form=form, transactions=transactions, current_sum=current_sum)

@bp.route('/del_transaction/<id>')
@login_required
def del_transaction(id):
    transaction = Transaction.query.filter_by(id=id).first_or_404()
    if (transaction.user.id == current_user.id):
        db.session.delete(transaction)
        db.session.commit()
        flash('Transaction deleted~')
        return redirect(url_for('wallet.my_wallet'))
    return redirect(url_for('wallet.my_wallet'))
