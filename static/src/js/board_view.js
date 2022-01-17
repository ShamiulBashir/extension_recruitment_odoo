custom_events: _.extend({}, FormController.prototype.custom_events, {
    _saveDashboard: function () {
        var board = this.renderer.getBoard();
        var arch = QWeb.render('DashBoard.xml', _.extend({}, board));
        console.log(12346)
        return this._rpc({
            route: '/web/view/edit_custom',
            params: {
                custom_id: this.customViewID != null ? this.customViewID : '',
                arch: arch,
                view_id: this.actionViews[0]['viewID']
            }
        }).then(dataManager.invalidate.bind(dataManager));
    }
})



