odoo.define('viseo_project_project.open_task', function (require) {
'use strict';
    // var core = require('web.core');
    // var Domain = require('web.Domain');
    var pyUtils = require('web.py_utils');
    var viewUtils = require('web.viewUtils');
    // var Widget = require('web.Widget');

    // var qweb = core.qweb;
    // var defaultViewTypes = ['gantt','kanban', 'tree'];
    var defaultViewTypes = ['kanban', 'tree'];
    const SEARCH_PANEL_LIMIT = 200;

    function _processSearchPanelNode(node, fields) {
        var sections = {};
        node.children.forEach((childNode, index) => {
            if (childNode.tag !== 'field') {
                return;
            }
            if (childNode.attrs.invisible === "1") {
                return;
            }
            var fieldName = childNode.attrs.name;
            var type = childNode.attrs.select === 'multi' ? 'filter' : 'category';

            var sectionId = _.uniqueId('section_');
            var section = {
                color: childNode.attrs.color,
                description: childNode.attrs.string || fields[fieldName].string,
                fieldName: fieldName,
                icon: childNode.attrs.icon,
                id: sectionId,
                index: index,
                type: type,
            };
            if (section.type === 'category') {
                section.icon = section.icon || 'fa-folder';
            } else if (section.type === 'filter') {
                section.disableCounters = !!pyUtils.py_eval(childNode.attrs.disable_counters || '0');
                section.domain = childNode.attrs.domain || '[]';
                section.groupBy = childNode.attrs.groupby;
                section.icon = section.icon || 'fa-filter';
            }
            sections[sectionId] = section;
        });
        return sections;
    }
    var SearchPanel = require('web.SearchPanel')
    var ExtendSearchPanel = SearchPanel.include({
    computeSearchPanelParams: function (viewInfo, viewType) {
        var searchPanelSections;
        var classes;
        if (viewInfo) {
            var arch = viewUtils.parseArch(viewInfo.arch);
            viewType = viewType === 'list' ? 'tree' : viewType;
            arch.children.forEach(function (node) {
                if (node.tag === 'searchpanel') {
                    var attrs = node.attrs;
                    var viewTypes = defaultViewTypes;
                    if (attrs.view_types) {
                        viewTypes = attrs.view_types.split(',');
                    }
                    if (attrs.class) {
                        classes = attrs.class.split(' ');
                    }
                    if (viewTypes.indexOf(viewType) !== -1) {
                        searchPanelSections = _processSearchPanelNode(node, viewInfo.fields);
                    }
                }
            });
        }
        return {
            sections: searchPanelSections,
            classes: classes,
        };
    },
    /**
     * @private
     * @param {string} categoryId
     * @param {Object[]} values
     */
    _createCategoryTree: function (categoryId, values) {
        var category = this.categories[categoryId];

        let parentField = category.parentField;
        if (values.length === SEARCH_PANEL_LIMIT) {
            category.limitAttained = true;
            if (parentField) {
                // we do not hierarchize values
                parentField = false;
            }
        }

        category.values = {};
        // console.log(this.model)
        _.each(values, function (value) {
            category.values[value.id] = _.extend({}, value, {
                childrenIds: [],
                folded: true,
                parentId: value[parentField] && value[parentField][0] || false,
            });
            // console.log(category.values[value.id])
        });

        _.map(values, function (value) {
            var value = category.values[value.id];
            var parentCategoryId = value.parentId;
            if (parentCategoryId && parentCategoryId in category.values) {
                category.values[parentCategoryId].childrenIds.push(value.id);
            }
        });
        category.rootIds = _.filter(_.map(values, function (value) {
            return value.id;
        }), function (valueId) {
            var value = category.values[valueId];
            return value.parentId === false;
        });

        // set active value
        var validValues = _.pluck(category.values, 'id').concat([false]);
        var value = this._getCategoryDefaultValue(category, validValues);
        category.activeValueId = _.contains(validValues, value) ? value : false;

        // unfold ancestor values of active value to make it is visible

        if (category.activeValueId) {
            var parentValueIds = this._getAncestorValueIds(category, category.activeValueId);
            parentValueIds.forEach(function (parentValue) {
                category.values[parentValue].folded = false;
            });
        }
    },
    _fetchCategories: function () {
    var self = this;
    var proms = Object.keys(this.categories).map(function (categoryId) {
        var category = self.categories[categoryId];
        var field = self.fields[category.fieldName];
        var categoriesProm;
        var argument;
        if (field.type === 'selection') {
            var values = field.selection.map(function (value) {
                return {id: value[0], display_name: value[1]};
            });
            categoriesProm = Promise.resolve(values);
        } else {
            //Get value of active url
            function parseURLParams(url){
                 var queryStart = url.indexOf("?") + 1,
                    queryEnd = url.indexOf("#") + 1 || url.length +1,
                    query = url.slice(queryStart, queryEnd - 1),
                    pairs = query.replace(/\+/g, " ").split("&"),
                    parms = {}, i, n, v, nv;
                 if (query === url || query === "") return;

                 for (i = 0; i < pairs.length; i++) {
                    nv = pairs[i].split("=", 2);
                    n = decodeURIComponent(nv[0]);
                    v = decodeURIComponent(nv[1]);
                    if (!parms.hasOwnProperty(n)) parms[n] = [];
                    parms[n].push(nv.length === 2 ? v : null);
                 }
                return parms;
            }
            var url = window.location.href;
            var page_url = url.replace('#', '?');
            var parms = parseURLParams(page_url);
            if (self.model === 'viseo.project.task'){
                if ('id' in parms){
                    var viseo_project_id = parseInt(parms.id);
                }else{
                    var elements = document.getElementsByClassName('o_search_panel_category_value');
                    var list_of_project = []
                    for (const item of elements){
                        list_of_project .push(item.getAttribute('data-id'))
                    }
                    var viseo_project_id = parseInt(list_of_project[1]);
                    // var project_id = parseInt(parms.active_id);
                }

                argument = [category.fieldName, viseo_project_id]

            }else{
                argument = [category.fieldName]
            };
            categoriesProm = self._rpc({
                method: 'search_panel_select_range',
                model: self.model,
                args: argument,
            }).then(function (result) {
                category.parentField = result.parent_field;
                return result.values;
            });
        }
        return categoriesProm.then(function (values) {
            self._createCategoryTree(categoryId, values);
        });
    });
    return Promise.all(proms);
    },
           /**
     * @private
     * @param {MouseEvent} ev
     */
    _onCategoryValueClicked: function (ev) {
        ev.stopPropagation();
        var $item = $(ev.currentTarget).closest('.o_search_panel_category_value');
        var category = this.categories[$item.data('categoryId')];
        var valueId = $item.data('id') || false;
            // call action if model project.task with actual active_id
        category.activeValueId = valueId;
        if (category.values[valueId]) {
            category.values[valueId].folded = !category.values[valueId].folded;
        };
        if (this.model === 'viseo.project.task') {
            this.do_action({
                name: category.values[valueId]["display_name"] || false,
                type: 'ir.actions.act_window',
                res_model: 'viseo.project.task',
                view_mode: 'tree',
                views: [[false, 'list'], [false, 'kanban'], [false, 'form']],
                // views: [[false, 'list'], [false, 'kanban'], [false, 'gantt'], [false, 'form'], [false, 'graph'], [false, 'calendar'], [false, 'pivot']],
                // binding_view_types: ['list','kanban','gantt'],
                // target: 'main',
                target: 'current',
                context: {'active_id':valueId, 'search_default_viseo_project_id': [valueId], 'default_viseo_project_id':valueId}
        });
        };
        // if (this.model != 'viseo.project.task'){
        //     category.activeValueId = valueId;
        // };
        if (category.values[valueId]) {
            category.values[valueId].folded = !category.values[valueId].folded;
        }
        var storageKey = this._getLocalStorageKey(category);
        this.call('local_storage', 'setItem', storageKey, valueId);
        this._notifyDomainUpdated();
    },

    })
});

