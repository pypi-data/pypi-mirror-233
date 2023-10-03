import requests
from requests.structures import CaseInsensitiveDict

from decouple import config
from einvoices.services.invoice_service import InvoiceService
from zatca.models import ZatcaLog


class ZatcaService:
    _url = config('ZATCA_URL')

    @staticmethod
    def _header():
        headers = CaseInsensitiveDict()
        headers["Accept-Version"] = "V2"
        headers["accept"] = "application/json"
        headers["Accept-Language"] = "en"
        headers["Content-Type"] = "application/json"

        return headers

    @classmethod
    def compliance_csid(cls, otp, csr):
        url = f'{cls._url}/compliance'

        headers = cls._header()
        headers["OTP"] = otp

        data = f'''
            {{
                "csr": "{csr}"
            }}
        '''

        response = requests.post(url=url, headers=headers, data=data)

        zatca_log = ZatcaLog(req={'url': url, 'request': data}, res=response.text,
                             status_code=response.status_code,
                             request_type=ZatcaLog.COMPLIANCE_CSID)
        zatca_log.save()

        if response.ok:
            return True, {'username': response.json()['binarySecurityToken'], 'password': response.json()['secret'],
                          'request_id': response.json()['requestID']}
        return False, None

    @classmethod
    def compliance_check(cls, invoice, username, password):
        url = f'{cls._url}/compliance/invoices'

        header = {**cls._header()}

        data = f'''
             {{
                "invoiceHash": "{invoice['invoiceHash']}",
                "uuid": "{invoice['uuid']}",
                "invoice": "{invoice['invoice']}"
            }}
        '''

        response = requests.post(url=url,
                                 auth=(username, password),
                                 headers=header,
                                 data=data)

        zatca_log = ZatcaLog(req={'url': url, 'request': data}, res=response.text,
                             status_code=response.status_code,
                             request_type=ZatcaLog.COMPLIANCE_CHECK)
        zatca_log.save()

        if response.ok:
            return response.json()['reportingStatus']

        return False

    @classmethod
    def production_csids_onboarding(cls, username, password, request_id):
        url = f'{cls._url}/production/csids'
        data = f'''
             {{
                
                "compliance_request_id": "{request_id}"
 
            }}
        '''

        response = requests.post(
            url=url, auth=(username, password), headers=cls._header(), data=data
        )

        zatca_log = ZatcaLog(req={'url': url, 'request': data}, res=response.text, status_code=response.status_code,
                             request_type=ZatcaLog.PRODUCTION_CSID_ONBOARDING)
        zatca_log.save()

        if response.ok:
            return True, {"username": response.json()['binarySecurityToken'], "password": response.json()['secret']}

        else:
            return False, None

    @classmethod
    def production_csids_renewing(cls, otp, csr, username, password):
        url = f'{cls._url}/production/csids'

        header = {**cls._header(), "OTP": otp}

        data = {
            "csr": csr
        }

        response = requests.patch(url=url, headers=header, data=data, auth=(username, password))

        zatca_log = ZatcaLog(req={'url': url, 'request': data}, res=response.text, status_code=response.status_code,
                             request_type=ZatcaLog.PRODUCTION_CSID_RENEWING)

        zatca_log.save()

        if response.ok:
            return True, {"username": response.json()['binarySecurityToken'], "password": response.json()['secret']}

        else:
            return False, None

    @classmethod
    def reporting_invoice(cls, invoice, username, password):
        """
            :invoice_uuid: invoice id
            :invoice: encoded invoice
        """

        url = f'{cls._url}/invoices/reporting/single'
        # Simplified invoice no need for clearance so, it will be 0

        data = f'''
             {{
                "invoiceHash": "{invoice.hash_key}",
                "uuid": "{invoice.id}",
                "invoice": "{invoice.encoded_zatca}"
            }}
        '''

        response = requests.post(url=url,
                                 headers=cls._header(),
                                 auth=(username, password),
                                 data=data)

        zatca_log = ZatcaLog(req={'url': url, 'request': data}, invoice_id=invoice.id, res=response.text,
                             status_code=response.status_code,
                             request_type=ZatcaLog.REPORTING_INVOICE)

        zatca_log.save()

        if response.ok or response.status_code == 201 or response.status_code == 400:
            # TODO is this part correct?  response.json()['warnings']
            return response.json()['reportingStatus'], response.json()['warnings'] is None
        else:
            pass

    #             reporter.bug

    @classmethod
    def invoice_clearance(cls, invoice, username, password):
        """
            @param invoice:
            @param username:
            @param password:
            @return:
        """

        url = f'{cls._url}/invoices/clearance/single'

        data = f'''
             {{
                "invoiceHash": "{invoice.hash_key}",
                "uuid": "{invoice.id}",
                "invoice": "{invoice.encoded_zatca}"
            }}
        '''

        response = requests.post(url=url,
                                 headers=cls._header(),
                                 auth=(username, password),
                                 data=data)

        zatca_log = ZatcaLog(req={'url': url, 'request': data}, invoice_id=invoice.id, res=response.text,
                             status_code=response.status_code,
                             request_type=ZatcaLog.REPORTING_INVOICE)

        zatca_log.save()
        # TODO manipulating the invoice QR code etc
        if response.ok or response.status_code == 201 or response.status_code == 400:
            if response.status_code == 200:
                encoded_invoice = response.json()['clearedInvoice']
                InvoiceService.store_b2b_invoice(invoice, encoded_invoice)
            return response.json()['clearanceStatus'], response.json()['warnings'] is None
