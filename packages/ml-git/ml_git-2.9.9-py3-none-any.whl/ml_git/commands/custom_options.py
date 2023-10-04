"""
© Copyright 2020-2022 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""
import click
from click import Option, UsageError, Command, MissingParameter

from ml_git import log
from ml_git.commands import prompt_msg
from ml_git.commands.wizard import wizard_for_field, is_wizard_enabled, choice_wizard_for_field
from ml_git.constants import MultihashStorageType, StorageType
from ml_git.ml_git_message import output_messages


class MutuallyExclusiveOption(Option):
    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop('mutually_exclusive', []))
        help = kwargs.get('help', '')
        if self.mutually_exclusive:
            ex_str = ', '.join(self.mutually_exclusive)
            kwargs['help'] = help + (
                    ' NOTE: Mutually exclusive with'
                    ' argument: ' + ex_str + '.'
            )
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise UsageError(
                'The argument `{}` is mutually exclusive with '
                'argument `{}`.'.format(
                    self.name,
                    ', '.join(self.mutually_exclusive)
                )
            )

        return super(MutuallyExclusiveOption, self).handle_parse_result(
            ctx,
            opts,
            args
        )


class OptionRequiredIf(Option):
    def __init__(self, *args, **kwargs):
        self.required_option = set(kwargs.pop('required_option', []))
        help = kwargs.get('help', '')
        if self.required_option:
            ex_str = ', '.join(self.required_option)
            kwargs['help'] = help + (' NOTE: This option is required if --' + ex_str + ' is used.')
        super(OptionRequiredIf, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        using_required_option = self.name in opts
        using_dependent_options = all(opt.replace('-', '_') in opts for opt in self.required_option)
        option_name = self.name.replace('_', '-')
        if not using_required_option and using_dependent_options:
            msg = output_messages['ERROR_REQUIRED_OPTION_MISSING'].format(option_name, ', '.join(self.required_option), option_name)
            if not is_wizard_enabled():
                raise MissingParameter(ctx=ctx, param=self, message=msg)
            requested_value = wizard_for_field(ctx, None, msg, required=True)
            opts[self.name] = requested_value
            return super(OptionRequiredIf, self).handle_parse_result(ctx, opts, args)
        elif using_required_option and not using_dependent_options:
            log.warn(output_messages['WARN_USELESS_OPTION'].format(option_name, ', '.join(self.required_option)))
        return super(OptionRequiredIf, self).handle_parse_result(ctx, opts, args)


class DeprecatedOption(Option):
    def __init__(self, *args, **kwargs):
        self.deprecated = kwargs.pop('deprecated', ())
        self.preferred = kwargs.pop('preferred', args[0][-1])
        help = kwargs.get('help', '')
        if self.deprecated:
            kwargs['help'] = help + (' [DEPRECATED:' + self.deprecated[0] + ']')
        super(DeprecatedOption, self).__init__(*args, **kwargs)


class DeprecatedOptionsCommand(Command):
    def make_parser(self, ctx):
        parser = super(DeprecatedOptionsCommand, self).make_parser(ctx)
        # get the parser options
        options = set(parser._short_opt.values())
        options |= set(parser._long_opt.values())

        for option in options:
            if not isinstance(option.obj, DeprecatedOption):
                continue

            def make_process(an_option):
                orig_process = an_option.process
                deprecated = getattr(an_option.obj, 'deprecated', None)
                preferred = getattr(an_option.obj, 'preferred', None)
                msg = "Expected `deprecated` value for `{}`"
                assert deprecated is not None, msg.format(an_option.obj.name)

                def process(value, state):
                    import inspect
                    frame = inspect.currentframe()
                    try:
                        opt = frame.f_back.f_locals.get('opt')
                    finally:
                        del frame
                    if opt in deprecated:
                        msg = "'{}' has been deprecated, use '{}' instead;"
                        log.warn(msg.format(opt, preferred))
                    return orig_process(value, state)
                return process
            option.process = make_process(option)
        return parser


def check_multiple(ctx, param, value):
    if len(value) == 0:
        return None, False
    elif len(value) > 1:
        raise click.BadParameter(output_messages['ERROR_OPTION_WITH_MULTIPLE_VALUES'].format(param))
    return value[0], False


def check_valid_storage_choice(ctx, param, value):
    local_enabled = ctx.params['wizard']
    if value and (value not in MultihashStorageType.to_list()):
        if local_enabled or is_wizard_enabled():
            return choice_wizard_for_field(ctx, None, prompt_msg.INVALID_STORAGE_TYPE_MESSAGE.format(value),
                                           click.Choice(MultihashStorageType.to_list()), default=StorageType.S3H.value,
                                           wizard_flag=local_enabled), True
        else:
            raise click.BadParameter(output_messages['ERROR_STORAGE_TYPE_INPUT_INVALID'].format(value))
    return value, False


def multiple_option_callback(callbacks, ctx, param, value):
    current_value = value
    callback = 0
    if len(callbacks) > 0:
        while callback != len(callbacks):
            new_value, wizard_been_used = callbacks[callback](ctx, param, current_value)
            if wizard_been_used:
                callback = 0
            else:
                callback += 1
            current_value = new_value
    return current_value


def check_empty_values(ctx, param, value):
    value_present = value is not None
    value_empty = str(value).strip() == '' if value_present else False
    if value_present and value_empty:
        local_enabled = 'wizard' in ctx.params and ctx.params['wizard']
        if local_enabled or is_wizard_enabled():
            error_message = output_messages['ERROR_INVALID_VALUE_FOR'] % (''.join(["--", param.name]),
                                                                          output_messages['ERROR_EMPTY_VALUE'])
            return wizard_for_field(ctx, None, '{}\n{}'.format(error_message, prompt_msg.NEW_VALUE), wizard_flag=local_enabled, default=''), True
        raise click.BadParameter(output_messages['ERROR_EMPTY_VALUE'])
    return value, False


def check_integer_value(ctx, param, value):
    value_present = value is not None
    if value_present:
        try:
            return int(value), False
        except ValueError:
            local_enabled = 'wizard' in ctx.params and ctx.params['wizard']
            if local_enabled or is_wizard_enabled():
                error_message = output_messages['ERROR_INVALID_VALUE_FOR'] % (''.join(["--", param.name]),
                                                                              output_messages['ERROR_NOT_INTEGER_VALUE'].format(value))
                return wizard_for_field(ctx, None, '{}\n{}'.format(error_message, prompt_msg.NEW_VALUE), wizard_flag=local_enabled, type=int, default=''), True
            raise click.BadParameter(output_messages['ERROR_NOT_INTEGER_VALUE'].format(value))
    return value, False


def check_default_value(ctx, param, value, default=None):
    return default if value is None else value, False


def check_number_range(ctx, param, value, min, max):
    value_present = value is not None
    numeric_value = value
    if value_present:
        try:
            numeric_value = int(value)
        except ValueError:
            numeric_value = None
        if numeric_value is not None and not (min <= int(value) <= max):
            raise click.BadParameter(output_messages['ERROR_VALUE_NOT_IN_RANGE'].format(value, min, max))
    return numeric_value, False
