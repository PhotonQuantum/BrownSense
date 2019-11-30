function(newDoc, oldDoc, userCtx) {
    if (~userCtx.roles.indexOf('_admin')) {
        log('Server admin change on document: ' + newDoc._id);
    } else if (~userCtx.roles.indexOf('sudoers')) {
        log('Sudoer change on document: ' + newDoc._id)
    } else {
        throw {
            'unauthorized': 'Only admin or sudoer can issue commands.'
        }
    }
}
