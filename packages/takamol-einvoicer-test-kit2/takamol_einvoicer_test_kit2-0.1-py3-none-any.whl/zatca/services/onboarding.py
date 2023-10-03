from decouple import config
from django.utils.termcolors import colorize
from takamol_einvoicer_test_kit2.zatca.integrations.zatca import ZatcaService

from takamol_einvoicer_test_kit2.zatca.models import ZatcaKey


class OnboardingService:
    _csr = config('ZATCA_CSR')
    _otp = config('ZATCA_OTP')

    @staticmethod
    def generate_temp_invoices():
        return [], [], []

    @classmethod
    def certificate(cls):
        # call compliance CSID (certificate)
        result, certificate = ZatcaService.compliance_csid(cls._otp, cls._csr)

        if result:
            ZatcaKey.objects.create(username=certificate['username'],
                                    password=certificate['password'],
                                    meta_data={"request_id": certificate['request_id']},
                                    type=ZatcaKey.COMPLIANCE_CSID)

            return True
        # TODO Reporter.bug("Obtaining the Certificate Failed")
        return False

    @classmethod
    def compliance_check(cls, username, password):
        # Generate 3 temp einvoices (Tax, Debit, Credit)
        tax_invoice, credit_invoice, debit_invoice = cls.generate_temp_invoices()

        # call compliance check X3
        if tax_invoice and credit_invoice and debit_invoice:
            tax_compliance_check = ZatcaService.compliance_check(tax_invoice, username, password)
            credit_compliance_check = ZatcaService.compliance_check(credit_invoice, username, password)
            debit_compliance_check = ZatcaService.compliance_check(debit_invoice, username, password)

            if tax_compliance_check == credit_compliance_check == debit_compliance_check == "REPORTED":
                return True
            else:
                error_message = "Compliance Check Failed: One or More Invoice Types Does Not Reported"
                # TODO Reporter.bug(error_message)
                return False

        else:
            error_message = "Compliance Check Failed: Tax, Credit, or Debit Invoice Does Not Exists"
            # TODO Reporter.bug(error_message)
            return False

    @classmethod
    def production_csid_onboarding(cls, username, password, request_id):
        # call onboarding API
        result, prod_csid = ZatcaService.production_csids_onboarding(username, password, request_id)

        # TODO decode certificate
        # TODO convert number of days into date
        if result:
            ZatcaKey.objects.create(username=prod_csid['username'],
                                    password=prod_csid['password'],

                                    type=ZatcaKey.PRODUCTION_CSID_ONBOARDING)
            return True

        else:
            error_message = "Onboarding Process Failed: Something Went Wrong"
            # TODO Reporter.bug(error_message)
            return False

    @classmethod
    def process(cls):
        # Here will start the onboarding process steps:
        print(colorize('*** Zatca Onboading Process Started ***', fg='white', bg='blue'))

        # Step1: create certificate
        certificate_result = cls.certificate()

        if certificate_result:
            print(colorize('*** Step 1  Certificate: Successfully Initiated ***', fg='green'))

            if key := ZatcaKey.objects.filter(
                    type=ZatcaKey.COMPLIANCE_CSID, active=True
            ).first():
                print(colorize('*** Step 2 Zatca Key: Has Been Found ***', fg='green'))

                if result := cls.compliance_check(
                        key.username, key.password
                ):
                    print(colorize("*** Step 3 compliance check (Validate) ***", fg='green'))
                    if result := cls.production_csid_onboarding(
                            key.username, key.password, key.meta_data['request_id']
                    ):
                        print(colorize("*** Step 4 Onboarding Process Succeeded ***", fg='green'))
                    else:
                        print(colorize("Step 4 Onboarding Process Failed: Something Went Wrong", fg='red'))
                else:
                    print(colorize('Step 3 compliance check (Validate) Failed', fg='red'))
            else:
                print(colorize('Step 2 Zatca Keys: The is no active key', fg='red'))
        else:
            print(colorize('Step 1 Certificate: Obtaining the Certificate Failed', fg='red'))
