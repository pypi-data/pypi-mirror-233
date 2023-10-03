from decouple import config

from takamol_einvoicer_test_kit2.zatca.integrations.zatca import ZatcaService
from takamol_einvoicer_test_kit2.zatca.models import ZatcaKey


class RenewingService:
    _csr = config('ZATCA_CSR')
    _otp = config('ZATCA_OTP')

    @classmethod
    def process(cls):

        # revoke prod CSID onboarding
        prev_key = ZatcaKey.objects.filter(type=ZatcaKey.PRODUCTION_CSID_ONBOARDING, active=True).first()
        prev_key.active = False
        prev_key.save()

        # call renewing API
        result, renew_csid = ZatcaService.production_csids_renewing(cls._otp, cls._csr, prev_key.username,
                                                                    prev_key.password)

        if result:
            ZatcaKey.objects.create(username=renew_csid['username'],
                                    password=renew_csid['password'],
                                    type=ZatcaKey.PRODUCTION_CSID_RENEWING)

            return "Renewing Process Succeeded"

        else:
            error_message = "Renewing Process Failed: CSID has not been issued"

        # TODO Reporter.bug(error_message)

        return error_message
