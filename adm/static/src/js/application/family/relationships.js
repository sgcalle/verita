odoo.define('adm.family.relationships', require => {
    "use strict";

    require('web.core');

    let counter = 0;

    function removeNewRelationship(event) {
        $(event.currentTarget).closest('[data-adm-rel]').remove();
    }

    function moveToOtherRelationship(event) {
        const relationRowEl = event.currentTarget.closest('[data-adm-rel]');
        const otherRelationListEl = document.getElementById('other_relationship_card_list');

        const selectRelationTypeEl = relationRowEl.querySelector('[data-adm-field="relationship_type_id"]');
        if (selectRelationTypeEl) {
            selectRelationTypeEl.value = null;
        }

        otherRelationListEl.appendChild(relationRowEl);
    }

    function appendNewRelationship(event) {
        counter--;

        const cssQueryTemplate = event.currentTarget.dataset.template;
        const cssQueryAppendTo = event.currentTarget.dataset.appendTo;

        const $clonedNewRelationshipTemplate = $(cssQueryTemplate).clone();

        const $buttonToggleCollapse = $clonedNewRelationshipTemplate.find('[data-toggle="collapse"]')
        $buttonToggleCollapse[0].dataset.target = $buttonToggleCollapse[0].dataset.target + counter.toString();

        const $divCollapse = $clonedNewRelationshipTemplate.find('.collapse');
        $divCollapse[0].id = $divCollapse[0].id + counter.toString();

        $clonedNewRelationshipTemplate.find('input[type="radio"]').each((i, elIputRadio) => {
             elIputRadio.name = elIputRadio.name + counter.toString();
        });
        // We remove the style display none
        $clonedNewRelationshipTemplate.removeAttr('style');
        $clonedNewRelationshipTemplate.removeClass('d-none');
        $clonedNewRelationshipTemplate.addClass('mt-4');

        const relationshipList = document.querySelector(cssQueryAppendTo);
        const newMany2manyRev = document.createElement('DIV');
        newMany2manyRev.dataset.admRel = "rel";
        $clonedNewRelationshipTemplate.appendTo(newMany2manyRev);
        $clonedNewRelationshipTemplate.find('.remove-relationship').on('click', removeNewRelationship);
        relationshipList.appendChild(newMany2manyRev);
    }

    $(document).ready(() => {
        $('.add-relationship').on('click', appendNewRelationship);
        $('.remove-relationship').on('click', removeNewRelationship);
        $('.move-other-relationship').on('click', moveToOtherRelationship);
    });

})