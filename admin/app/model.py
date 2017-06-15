import enum
from app import db
from sqlalchemy.ext.hybrid import hybrid_property

class Base(db.Model):
    """
    Define a base model for other database tables to inherit
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

########################## Models ################################
class Machine(Base):
    __tablename__ = 'machine'
    name = db.Column(db.String, nullable=False, unique=True)
    status = db.Column(db.Enum('OFF', 'ON', 'BUSY', 'BROKEN'), nullable=False)
    power_in_kilowatt = db.Column(db.Integer) 
    photo = db.Column(db.String)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            status=self.status,
            power_in_kilowatt=self.power_in_kilowatt,
            photo=self.photo,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat()
        )

    def __repr__(self):
        return '%d - %s' % (self.id, self.name)

class Color(db.Model):
    """
    class doc
    """
    __tablename__ = 'color'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    name = db.Column(db.String, nullable=False, unique=True)
    color_code = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return '%d - %s' % (self.id, self.name)

#m-m mapping
product_colors_table = db.Table(
    'product_color',
    db.Model.metadata,
    db.Column('product_id', db.String, db.ForeignKey('product.id')),
    db.Column('color_id', db.String, db.ForeignKey('color.id'))
)

"""
class Product(Base):
# m-m
    colors = db.relationship(
        'Color',
        secondary=colors,
        backref=db.backref('products', lazy='dynamic')
    )
"""

class Product(Base):
    '''Model for product table'''
    __tablename__ = 'product'
    name = db.Column(db.String, nullable=False, unique=True)
    weight = db.Column(db.Integer, nullable=False)
    time_to_build = db.Column(db.Integer, nullable=False)
    selling_price = db.Column(db.Integer)
    num_employee_required = db.Column(db.Integer, nullable=False)
    mold_id = db.Column(db.Integer)
    photo = db.Column(db.String)
    multi_colors_ratio = db.Column(db.String)
    colors = db.relationship(Color, secondary=product_colors_table)
    machine_id = db.Column(db.Integer, db.ForeignKey(Machine.id), nullable=False)
    machine = db.relationship(Machine, backref='machine')

    def __repr__(self):
        return '%d - %s' % (self.id, self.name)


class Order(Base):
    """Order table ORM mapping"""
    __tablename__ = 'order'
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.Enum('AUTO_PLAN', 'MANUAL_PLAN', 'READY', 'IN_PROGRESS', 'COMPLETED', 'SHIPPED'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    quantity_completed = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=False)
    product = db.relationship(Product, backref='product')
    raw_material_quantity = db.Column(db.Integer, nullable=False)
    is_raw_material_checkout = db.Column(db.Boolean, nullable=False, default=False)
    estimated_time_to_complete = db.Column(db.Integer, nullable=False)
    production_start_at = db.Column(db.DateTime)
    production_end_at = db.Column(db.DateTime)
    note = db.Column(db.String)
    assigned_machine_id = db.Column(db.Integer, db.ForeignKey(Machine.id))
    # NOTE: backref name MUST be unique between relationships.
    assigned_machine = db.relationship(Machine, backref='order_to_machine')


    def __init__(self):
        self.is_raw_material_checkout = False


    def __repr__(self):
        return '%d - %s' % (self.id, self.name)


    @hybrid_property
    def photo(self):
        return self.product.photo


class Shift(db.Model):
    __tablename__ = 'shift'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    shift_name = db.Column(db.String, nullable=False, unique=True)
    start_hour = db.Column(db.Integer, nullable=False)
    end_hour = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '%s %s - %s' % (self.shift_name, self.toAM_PM(self.start_hour), self.toAM_PM(self.end_hour))

    def toAM_PM(self, hour):
        if hour == 12:
            return "12P.M"
        elif hour > 12:
            return "%dP.M" % (hour-12)
        else:
            return "%dA.M" % (hour)


class ProductionEntry(db.Model):
    __tablename__ = 'production_entry'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    shift_id = db.Column(db.Integer, db.ForeignKey(Shift.id), nullable=False)
    shift = db.relationship(Shift, backref='production_entry_shift')
    order_id = db.Column(db.Integer, db.ForeignKey(Order.id), nullable=False)
    order = db.relationship(Order, backref='production_entry_order')
    team_lead_name = db.Column(db.String)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    h_1_am_num_good = db.Column(db.Integer)
    _1_am_num_bad = db.Column(db.Integer)
    _2_am_num_good = db.Column(db.Integer)
    _2_am_num_bad = db.Column(db.Integer)
    _3_am_num_good = db.Column(db.Integer)
    _3_am_num_bad = db.Column(db.Integer)
    _4_am_num_good = db.Column(db.Integer)
    _4_am_num_bad = db.Column(db.Integer)
    _5_am_num_good = db.Column(db.Integer)
    _5_am_num_bad = db.Column(db.Integer)
    _6_am_num_good = db.Column(db.Integer)
    _6_am_num_bad = db.Column(db.Integer)
    _7_am_num_good = db.Column(db.Integer)
    _7_am_num_bad = db.Column(db.Integer)
    _8_am_num_good = db.Column(db.Integer)
    _8_am_num_bad = db.Column(db.Integer)
    _9_am_num_good = db.Column(db.Integer)
    _9_am_num_bad = db.Column(db.Integer)
    _10_am_num_good = db.Column(db.Integer)
    _10_am_num_bad = db.Column(db.Integer)
    _11_am_num_good = db.Column(db.Integer)
    _11_am_num_bad = db.Column(db.Integer)
    _12_pm_num_good = db.Column(db.Integer)
    _12_pm_num_bad = db.Column(db.Integer)
    _1_pm_num_good = db.Column(db.Integer)
    _1_pm_num_bad = db.Column(db.Integer)
    _2_pm_num_good = db.Column(db.Integer)
    _2_pm_num_bad = db.Column(db.Integer)
    _3_pm_num_good = db.Column(db.Integer)
    _3_pm_num_bad = db.Column(db.Integer)
    _4_pm_num_good = db.Column(db.Integer)
    _4_pm_num_bad = db.Column(db.Integer)
    _5_pm_num_good = db.Column(db.Integer)
    _5_pm_num_bad = db.Column(db.Integer)
    _6_pm_num_good = db.Column(db.Integer)
    _6_pm_num_bad = db.Column(db.Integer)
    _7_pm_num_good = db.Column(db.Integer)
    _7_pm_num_bad = db.Column(db.Integer)
    _8_pm_num_good = db.Column(db.Integer)
    _8_pm_num_bad = db.Column(db.Integer)
    _9_pm_num_good = db.Column(db.Integer)
    _9_pm_num_bad = db.Column(db.Integer)
    _10_pm_num_good = db.Column(db.Integer)
    _10_pm_num_bad = db.Column(db.Integer)
    _11_pm_num_good = db.Column(db.Integer)
    _11_pm_num_bad = db.Column(db.Integer)
        
    @hybrid_property
    def total_good(self):
        return (
            self.h_1_am_num_good + self._2_am_num_good + self._3_am_num_good + self._4_am_num_good + 
            self._5_am_num_good + self._6_am_num_good + self._7_am_num_good + self._8_am_num_good + 
            self._9_am_num_good + self._10_am_num_good + self._11_am_num_good + self._12_pm_num_good +
            self._1_pm_num_good + self._2_pm_num_good + self._3_pm_num_good + self._4_pm_num_good + 
            self._5_pm_num_good + self._6_pm_num_good + self._7_pm_num_good + self._8_pm_num_good + 
            self._9_pm_num_good + self._10_pm_num_good + self._11_pm_num_good
        )

    @hybrid_property
    def total_bad(self):
        return (
            self._1_am_num_bad + self._2_am_num_bad + self._3_am_num_bad + self._4_am_num_bad + 
            self._5_am_num_bad + self._6_am_num_bad + self._7_am_num_bad + self._8_am_num_bad + 
            self._9_am_num_bad + self._10_am_num_bad + self._11_am_num_bad + self._12_pm_num_bad +
            self._1_pm_num_bad + self._2_pm_num_bad + self._3_pm_num_bad + self._4_pm_num_bad + 
            self._5_pm_num_bad + self._6_pm_num_bad + self._7_pm_num_bad + self._8_pm_num_bad + 
            self._9_pm_num_bad + self._10_pm_num_bad + self._11_pm_num_bad
        )
    

############ ORM Triggers #############
from sqlalchemy.event import listens_for
from decimal import *

@listens_for(Order, 'before_insert')
def del_image(mapper, connection, target):
    print "%%%%%%%% before_insert_order %%%%%%%%%%"
    # 1. Calculate number of raw material bags.
    weight = Decimal(target.product.weight)
    total_weight = Decimal(target.quantity) * weight
    # TODO: need to define as constant
    raw_weight_per_bag = 500
    num_raw_bag = Decimal(total_weight) / raw_weight_per_bag
    # round results to fixed number
    target.raw_material_quantity = int(Decimal(num_raw_bag).quantize(Decimal('1.'), rounding=ROUND_UP))
    print "1. num_raw_bag = %d" % target.raw_material_quantity

    # 2. Calculate estimated time to complete
    target.estimated_time_to_complete = target.quantity * target.product.time_to_build
    print "2. Estimated time to complete = %d sec" % target.estimated_time_to_complete
    
    # 3. Set the mode based on the machine id is default or not.
    target.status = 'MANUAL_PLAN'
    if not target.assigned_machine_id:
        target.assigned_machine_id = target.product.machine_id
        target.status = 'AUTO_PLAN'
    

@listens_for(Order, 'before_update')
def del_image(mapper, connection, target):
    print "%%%%%%%% before_update_order %%%%%%%%%%"
    # 1. Calculate number of raw material bags.
    
    for s in ('IN_PROGRESS', 'COMPLETED', 'SHIPPED'):
        if target.status == s:
            print "Invalid state. Changes cannot be made."

    if target.quantity_completed >= target.quantity:
        target.status = 'COMPLETED'
        print "Order completed"

    if target.is_raw_material_checkout:
        target.status = 'READY'
    
    if target.assigned_machine_id is not target.product.machine_id:
        target.status = 'MANUAL_PLAN'