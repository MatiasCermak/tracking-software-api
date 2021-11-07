from django.db import models


class Project(models.Model):
    code_name = models.CharField('Código', max_length=255)
    software_name = models.CharField('Nombre de software', max_length=255)
    software_version = models.CharField('Versión de software', max_length=100)
    active = models.BooleanField('Estado', default=True)
    # owner: Foreing Key - Usuario dueño del proyecto
    # client: Foreing Key - Cliente que encargó el proyecto


class Ticket(models.Model):
    NEW = 0
    IN_PROGRESS = 1
    ON_REVISION = 2
    ON_HOLD = 3
    CLOSED = 4
    STATES = (
        (NEW, "Nuevo"),
        (IN_PROGRESS, "En progreso"),
        (ON_REVISION, "En revisión"),
        (ON_HOLD, "En espera"),
        (CLOSED, "Cerrado"),
    )

    state = models.SmallIntegerField('Estado', default=NEW, choices=STATES)
    description = models.CharField('Descripción', max_length=255)
    title = models.CharField('Título', max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Proyecto',
                                default=0, related_name='tickets')
    # created_by/user: Foreing Key - Usuario que lo creó
    # area: Foreing Key - Área a la que pertenece


class Ticket_Detail(models.Model):
    description = models.CharField('Descripción', max_length=255)
    title = models.CharField('Título', max_length=100)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='Ticket',
                               default=0, related_name='details')
    # user: Foreing Key - Usuario que lo creó
