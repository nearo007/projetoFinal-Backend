from .admin_controller import admin_bp
from .api_controller import api_bp
from .teacher_controller import teacher_bp
from .user_controller import user_bp

controllers = [admin_bp, api_bp, teacher_bp, user_bp]