"""
Page Object para a página de Checkout (Pagamento do Link).

Este módulo contém a classe que encapsula as interações com o formulário
de pagamento quando o link é acessado.
"""
import time
from tests.page_objects.base_page import BasePage
from tests.locators.payment_link_checkout_locators import PaymentLinkCheckoutLocators

class PaymentLinkCheckoutPage(BasePage):
    """Classe que representa a página de checkout do link de pagamento."""
    
    def __init__(self, driver):
        """Inicializa a página de checkout."""
        super().__init__(driver)
        self.logger.info("Inicializada PaymentLinkCheckoutPage")
        
    # --- MÉTODOS DE PREENCHIMENTO DE DADOS DO COMPRADOR ---
    
    def fill_buyer_name(self, name: str):
        """Preenche o campo de nome completo do comprador."""
        self.fill_input(PaymentLinkCheckoutLocators.NAME_INPUT, name)
        self.logger.info(f"Preencheu nome: {name}")
    
    def fill_buyer_email(self, email: str):
        """Preenche o campo de e-mail do comprador."""
        self.fill_input(PaymentLinkCheckoutLocators.EMAIL_INPUT, email)
        self.logger.info(f"Preencheu e-mail: {email}")
    
    def fill_buyer_document(self, document: str):
        """Preenche o campo de CPF ou CNPJ do comprador."""
        self.fill_input(PaymentLinkCheckoutLocators.DOCUMENT_INPUT, document)
        self.logger.info(f"Preencheu documento: {document}")
    
    def fill_buyer_phone(self, phone: str):
        """Preenche o campo de celular do comprador."""
        import time
        
        self.logger.info(f"Preenchendo telefone: {phone}")
        
        time.sleep(3)
        
        # JavaScript que busca por NAME e PLACEHOLDER (não por ID!)
        script = """
        var inputs = document.querySelectorAll('input[name="phone"][placeholder*="99"]');
        var preenchido = false;
        
        for (var i = 0; i < inputs.length; i++) {
            var input = inputs[i];
            
            // Verifica se está visível
            if (input.offsetWidth > 0 && input.offsetHeight > 0) {
                input.focus();
                input.value = arguments[0];
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
                input.dispatchEvent(new Event('keyup', { bubbles: true }));
                input.blur();
                
                preenchido = true;
                console.log('Telefone preenchido:', input.value);
                break;
            }
        }
        
        return preenchido;
        """
        
        resultado = self.driver.execute_script(script, phone)
        
        time.sleep(1)
        
        if resultado:
            self.logger.info(f"✅ Telefone preenchido: {phone}")
        else:
            raise Exception("Campo telefone não foi preenchido")

    # --- MÉTODOS DE SELEÇÃO DE FORMA DE PAGAMENTO ---
    
    def select_credit_card_payment(self):
        """Seleciona a opção de pagamento com cartão de crédito."""
        import time
        
        self.logger.info("Selecionando cartão de crédito...")
        
        time.sleep(2)
        
        # JavaScript para clicar no radio button de crédito
        script = """
        // Tenta por ID primeiro
        var radio = document.getElementById('creditCard');
        if (radio && radio.offsetWidth > 0) {
            radio.click();
            return true;
        }
        
        // Tenta por value
        var radios = document.querySelectorAll('input[type="radio"][value*="credit"]');
        for (var i = 0; i < radios.length; i++) {
            if (radios[i].offsetWidth > 0 || radios[i].offsetHeight > 0) {
                radios[i].click();
                return true;
            }
        }
        
        // Tenta clicar no label
        var labels = document.querySelectorAll('label');
        for (var i = 0; i < labels.length; i++) {
            if (labels[i].textContent.includes('Cartão') || labels[i].textContent.includes('crédito')) {
                labels[i].click();
                return true;
            }
        }
        
        return false;
        """
        
        resultado = self.driver.execute_script(script)
        
        time.sleep(1)
        
        if resultado:
            self.logger.info("✅ Cartão de crédito selecionado")
        else:
            raise Exception("Não conseguiu selecionar cartão de crédito")
    
    def select_pix_payment(self):
        """Seleciona a opção de pagamento com Pix."""
        self.click(PaymentLinkCheckoutLocators.PIX_RADIO)
        self.logger.info("Selecionou forma de pagamento: Pix")
        time.sleep(1)
        
        # --- MÉTODOS DE PREENCHIMENTO DE DADOS DO CARTÃO ---
    
    def fill_card_number(self, card_number: str):
        """Preenche o número do cartão de crédito."""
        self.fill_input(PaymentLinkCheckoutLocators.CARD_NUMBER_INPUT, card_number)
        self.logger.info(f"Preencheu número do cartão: {card_number[:4]}****{card_number[-4:]}")
    
    def fill_card_validity(self, validity: str):
        """Preenche a validade do cartão (MM/AA)."""
        self.fill_input(PaymentLinkCheckoutLocators.CARD_VALIDITY_INPUT, validity)
        self.logger.info(f"Preencheu validade: {validity}")
    
    def fill_card_cvv(self, cvv: str):
        """Preenche o código de segurança (CVV) do cartão."""
        self.fill_input(PaymentLinkCheckoutLocators.CARD_CVV_INPUT, cvv)
        self.logger.info("Preencheu CVV")
    
    def fill_card_holder_name(self, name: str):
        """Preenche o nome impresso no cartão."""
        self.fill_input(PaymentLinkCheckoutLocators.CARD_NAME_INPUT, name)
        self.logger.info(f"Preencheu nome no cartão: {name}")
    
    def fill_card_holder_document(self, document: str):
        """Preenche o CPF do portador do cartão."""
        self.fill_input(PaymentLinkCheckoutLocators.CARD_HOLDER_DOCUMENT_INPUT, document)
        self.logger.info(f"Preencheu CPF do portador: {document}")
        
        # --- MÉTODOS DE PREENCHIMENTO DE ENDEREÇO ---
    
    def fill_zip_code(self, zip_code: str):
        """Preenche o campo de CEP."""
        import time
        
        self.logger.info(f"Preenchendo CEP: {zip_code}")
        
        time.sleep(2)
        
        # JavaScript para preencher CEP (igual ao telefone que funcionou!)
        script = """
        var inputs = document.querySelectorAll('input[id="zipCode"], input[name="zipCode"]');
        var preenchido = false;
        
        for (var i = 0; i < inputs.length; i++) {
            var input = inputs[i];
            
            // Verifica se está visível
            if (input.offsetWidth > 0 && input.offsetHeight > 0) {
                input.focus();
                input.value = arguments[0];
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
                input.dispatchEvent(new Event('keyup', { bubbles: true }));
                input.blur();
                
                preenchido = true;
                console.log('CEP preenchido:', input.value);
                break;
            }
        }
        
        return preenchido;
        """
        
        resultado = self.driver.execute_script(script, zip_code)
        
        time.sleep(3)  # Aguarda busca automática do CEP
        
        if resultado:
            self.logger.info(f"✅ CEP preenchido: {zip_code}")
        else:
            raise Exception("Campo CEP não foi preenchido")

    
    def fill_street(self, street: str):
        """Preenche o campo de logradouro."""
        self._fill_address_field('street', street, 'Logradouro')

    def fill_street_number(self, number: str):
        """Preenche o campo de número do endereço."""
        import time
        
        self.logger.info(f"Preenchendo número: {number}")
        
        time.sleep(1)
        
        # JavaScript para preencher número (mesma técnica!)
        script = """
        var inputs = document.querySelectorAll('input[id="number"], input[name="number"]');
        var preenchido = false;
        
        for (var i = 0; i < inputs.length; i++) {
            var input = inputs[i];
            
            // Verifica se está visível
            if (input.offsetWidth > 0 && input.offsetHeight > 0) {
                input.focus();
                input.value = arguments[0];
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
                input.dispatchEvent(new Event('keyup', { bubbles: true }));
                input.blur();
                
                preenchido = true;
                console.log('Número preenchido:', input.value);
                break;
            }
        }
        
        return preenchido;
        """
        
        resultado = self.driver.execute_script(script, number)
        
        time.sleep(0.5)
        
        if resultado:
            self.logger.info(f"✅ Número preenchido: {number}")
        else:
            self.logger.warning(f"⚠️ Número não preenchido")
            raise Exception("Campo número não foi preenchido")

    def fill_complement(self, complement: str):
        """Preenche o campo de complemento."""
        self._fill_address_field('complement', complement, 'Complemento')

    def fill_neighborhood(self, neighborhood: str):
        """Preenche o campo de bairro."""
        self._fill_address_field('neighborhood', neighborhood, 'Bairro')

    def fill_city(self, city: str):
        """Preenche o campo de cidade."""
        self._fill_address_field('city', city, 'Cidade')

    def fill_state(self, state: str):
        """Preenche o campo de UF."""
        self._fill_address_field('stateCode', state, 'UF')

    def _fill_address_field(self, field_id: str, value: str, label: str):
        """Método helper para preencher campos de endereço."""
        import time
        time.sleep(0.5)
        
        script = f"""
        var input = document.getElementById('{field_id}');
        if (input && input.offsetWidth > 0) {{
            input.focus();
            input.value = arguments[0];
            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
            input.dispatchEvent(new Event('change', {{ bubbles: true }}));
            return true;
        }}
        return false;
        """
        
        resultado = self.driver.execute_script(script, value)
        
        if resultado:
            self.logger.info(f"✅ {label} preenchido: {value}")
        else:
            self.logger.warning(f"⚠️ {label} não preenchido (pode ter sido auto-preenchido pelo CEP)")
    
    def click_pay_now(self):
        """Clica no botão 'Pagar agora' para finalizar o pagamento."""
        self.click(PaymentLinkCheckoutLocators.PAY_NOW_BUTTON)
        self.logger.info("Clicou em 'Pagar agora'")
        time.sleep(5)
        
        # --- MÉTODOS HELPER ---
    
    def fill_buyer_info(self, name: str, email: str, document: str, phone: str):
        """Preenche todos os dados do comprador de uma vez."""
        self.fill_buyer_name(name)
        self.fill_buyer_email(email)
        self.fill_buyer_document(document)
        self.fill_buyer_phone(phone)
        self.logger.info("Dados do comprador preenchidos")
    
    def fill_card_info(self, card_number: str, validity: str, cvv: str, holder_name: str, holder_document: str):
        """Preenche todos os dados do cartão de uma vez."""
        self.fill_card_number(card_number)
        self.fill_card_validity(validity)
        self.fill_card_cvv(cvv)
        self.fill_card_holder_name(holder_name)
        self.fill_card_holder_document(holder_document)
        self.logger.info("Dados do cartão preenchidos")
    
    def fill_address_info(self, zip_code: str, street: str, number: str, neighborhood: str, city: str, state: str, complement: str = ""):
        """Preenche todos os dados de endereço de uma vez."""
        self.fill_zip_code(zip_code)
        
        # Verifica se os campos foram preenchidos automaticamente pelo CEP
        if not self.find_element(PaymentLinkCheckoutLocators.STREET_INPUT).get_attribute('value'):
            self.fill_street(street)
            self.fill_neighborhood(neighborhood)
            self.fill_city(city)
            self.fill_state(state)
        
        self.fill_street_number(number)
        if complement:
            self.fill_complement(complement)
        
        self.logger.info("Dados de endereço preenchidos")
        
    def complete_payment(self, buyer_data: dict, card_data: dict, address_data: dict):
        """
        Método master que completa todo o fluxo de pagamento.
        
        Este método executa TODAS as etapas necessárias para fazer um pagamento:
        1. Preenche dados do comprador
        2. Seleciona cartão de crédito
        3. Preenche dados do cartão
        4. Preenche endereço
        5. Clica em "Pagar agora"
        
        Returns:
            bool: True se conseguiu preencher tudo e clicar em pagar
        """
        try:
            # 1. Preenche dados do comprador
            self.fill_buyer_info(
                buyer_data['name'],
                buyer_data['email'],
                buyer_data['document'],
                buyer_data['phone']
            )
            
            # 2. Seleciona cartão de crédito
            self.select_credit_card_payment()
            
            # 3. Preenche dados do cartão
            self.fill_card_info(
                card_data['number'],
                card_data['validity'],
                card_data['cvv'],
                card_data['holder_name'],
                card_data['holder_document']
            )
            
            # 4. Preenche endereço
            self.fill_address_info(
                address_data['zip_code'],
                address_data['street'],
                address_data['number'],
                address_data['neighborhood'],
                address_data['city'],
                address_data['state'],
                address_data.get('complement', '')
            )
            
            # 5. Finaliza pagamento
            self.click_pay_now()
            
            self.logger.info("Pagamento completo realizado com sucesso")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao completar pagamento: {str(e)}")
            return False