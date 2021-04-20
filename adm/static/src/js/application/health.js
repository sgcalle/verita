odoo.define('adm.application.condition', require => {

    require('web.core');

    let counter = 0;

    function toggleHealthElementSelect(event) {
			const $otherToggleCheckbox = $(event.currentTarget);
			const $selectHealth = $otherToggleCheckbox.closest('div.row').find('select.js_select_health');
			const $inputHealth = $otherToggleCheckbox.closest('div.row').find('input.js_select_health');

			const isChecked = $otherToggleCheckbox.is(':checked');

			$selectHealth.toggle(!isChecked);
			$selectHealth.prop('disabled', isChecked);

			$inputHealth.toggle(isChecked);
			$inputHealth.prop('disabled', !isChecked);
	}

    function removeHealthElement(event) {
        $(event.currentTarget).closest('[data-adm-rel]').remove();
    }

    function appendNewHealthElement(type){
        counter--;
        const $clonedNewConditionTemplate = $(document.getElementById('template_' + type)).clone();
        // We remove the style display none
        $clonedNewConditionTemplate.removeAttr( 'style');

        // Change id and fors
        $clonedNewConditionTemplate.find('[id]').each((i, el) => {
            el.setAttribute('id', el.getAttribute('id') + counter);
        })
        $clonedNewConditionTemplate.find('[for]').each((i, el) => {
            el.setAttribute('for', el.getAttribute('for') + counter);
        });

        $clonedNewConditionTemplate.find('.js_' + type + '_toggle').on('change', toggleHealthElementSelect);
        $clonedNewConditionTemplate.find('input.js_select_health').hide().prop('disabled', true);

        const conditionList = document.getElementById(type + '_list');
        const newMany2manyRev = document.createElement('DIV');
        newMany2manyRev.dataset.admRel = "rel";
        $clonedNewConditionTemplate.appendTo(newMany2manyRev);
        $clonedNewConditionTemplate.find('.remove-rel-medical').on('click', removeHealthElement);
        // newMany2manyRev.appendChild(clonedNewConditionTemplate)
        conditionList.appendChild(newMany2manyRev);
    }

    $(document).ready(event => {
        $('.add-condition').on('click', () => appendNewHealthElement('condition'));
        $('.remove-rel-medical').on('click', removeHealthElement);

        $('.js_condition_select').on('change', toggleHealthElementSelect);
        $('.js_allergy_toggle').on('change', toggleHealthElementSelect);
        $('.js_medication_toggle').on('change', toggleHealthElementSelect);

        $('button.add-medical_condition').on('click', () => appendNewHealthElement('condition'));
        $('button.add-medical_allergy').on('click', () => appendNewHealthElement('allergy'));
        $('button.add-medical_medication').on('click', () => appendNewHealthElement('medication'));
    });

});