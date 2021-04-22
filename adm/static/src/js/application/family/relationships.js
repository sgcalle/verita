odoo.define('adm.family.relationships', require => {
    "use strict";

    require('web.core');
    const Dialog = require('web.Dialog');
    let counter = 0;

    function removeNewRelationship(event) {
        $(event.currentTarget).closest('[data-adm-rel]').remove();
    }

    function moveToOtherRelationship(event) {
        const relationRowEl = event.currentTarget.closest('[data-adm-rel]');
        const moveToSelector = event.currentTarget.dataset.target;
        const toggleTab = event.currentTarget.dataset.toggleTab;
        const relationType = event.currentTarget.dataset.relationType;
        const otherRelationListEl = document.querySelector(moveToSelector);

        const relationshipLimit = otherRelationListEl.dataset.relationshipLimit;
        const relationshipLimitMsm = otherRelationListEl.dataset.relationshipLimitMsm;

        if (!parseInt(relationshipLimit)
            || otherRelationListEl.querySelectorAll('[data-adm-rel]').length < parseInt(relationshipLimit)) {
            const selectRelationTypeEl = relationRowEl.querySelector('[data-adm-field="relationship_type_id"]');
            otherRelationListEl.appendChild(relationRowEl);
            const $tab = $(toggleTab);
            $tab.tab('show');

            // Get options depending on tab
            if (selectRelationTypeEl) {
                let option = null;
                switch (relationType) {
                    case 'parent':
                        option = _.filter(selectRelationTypeEl.options, opt => !opt.classList.contains('o_adm_hide_if_parent'))[1];
                        break;
                    case 'sibling':
                        option = _.filter(selectRelationTypeEl.options, opt => !opt.classList.contains('o_adm_hide_if_sibling'))[1];
                        break;
                    default:
                        option = selectRelationTypeEl.options[0];
                        break;
                }
                if (option) {
                    selectRelationTypeEl.value = option.value;
                }
            }
        } else {
            Dialog.alert(this, relationshipLimitMsm);
        }

    }

    function appendNewRelationship(event) {
        counter--;

        const currentTargetEl = event.currentTarget;
        const targetDataset = currentTargetEl.dataset;

        const cssQueryTemplate = targetDataset.template;
        const cssQueryAppendTo = targetDataset.appendTo;

        const relationshipListEl = document.querySelector(cssQueryAppendTo);

        if (relationshipListEl) {
            const relationshipLimit = relationshipListEl.dataset.relationshipLimit;
            const relationshipLimitMsm = relationshipListEl.dataset.relationshipLimitMsm;
            if (!parseInt(relationshipLimit)
                || relationshipListEl.querySelectorAll('[data-adm-rel]').length < parseInt(relationshipLimit)) {
                const $clonedNewRelationshipTemplate = $(cssQueryTemplate).clone();

                const $buttonToggleCollapse = $clonedNewRelationshipTemplate.find('[data-toggle="collapse"]')
                $buttonToggleCollapse[0].dataset.target = $buttonToggleCollapse[0].dataset.target + counter.toString();

                $clonedNewRelationshipTemplate.find('[id]').each((i, el) => {
                    el.id = el.id + counter.toString();
                })
                $clonedNewRelationshipTemplate.find('[for]').each((i, el) => {
                    el.setAttribute('for', el.getAttribute('for') + counter.toString())
                })
                $clonedNewRelationshipTemplate.find('[name]').each((i, el) => {
                    el.setAttribute('name', el.getAttribute('name') + counter.toString())
                })

                $clonedNewRelationshipTemplate.find('input[type="radio"]').each((i, elIputRadio) => {
                    elIputRadio.name = elIputRadio.name + counter.toString();
                });
                // We remove the style display none
                $clonedNewRelationshipTemplate.removeAttr('style');
                $clonedNewRelationshipTemplate.removeAttr('id');
                $clonedNewRelationshipTemplate.removeClass('d-none');
                $clonedNewRelationshipTemplate.addClass('mt-4');

                const newMany2manyRev = document.createElement('DIV');
                newMany2manyRev.dataset.admRel = "rel";
                $clonedNewRelationshipTemplate.appendTo(newMany2manyRev);
                $clonedNewRelationshipTemplate.find('.remove-relationship').on('click', removeNewRelationship);
                $clonedNewRelationshipTemplate.find('.move-relationship').on('click', moveToOtherRelationship);

                // Just a friky effect to make it cool ;)
                const $shownRelationShipCollapse = $(relationshipListEl).find('.collapse.show');

                // Hide shown relations

                function smoothScroll() {
                    $("html, body").animate({scrollTop: $clonedNewRelationshipTemplate.offset().top - 120}, 800);
                }

                relationshipListEl.appendChild(newMany2manyRev);
                if ($shownRelationShipCollapse.length) {
                    $shownRelationShipCollapse.on('hidden.bs.collapse', () => {
                        $shownRelationShipCollapse.off('hidden.bs.collapse');
                        smoothScroll();
                    }).collapse('hide');
                    $clonedNewRelationshipTemplate.find('.collapse').collapse('show');
                } else {
                    $clonedNewRelationshipTemplate.find('.collapse').collapse('show');
                    smoothScroll();
                }
            } else {
                Dialog.alert(this, relationshipLimitMsm);
            }
        }
    }

    $(document).ready(() => {
        $('.add-relationship').on('click', appendNewRelationship);
        $('.remove-relationship').on('click', removeNewRelationship);
        $('.move-relationship').on('click', moveToOtherRelationship);
    });

})