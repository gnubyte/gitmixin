# Git Mixin PoC

Main idea: a SQLALchemy mixin that can track individual fields and turn them into git repos with simple advance forward, rewind back mechanisms.

[Git Repo](https://gitlab.verizon.com/hastpa6/gitmixin)

## Testing

Finally wrote tests because the inline code when directly executing libs was getting out of hand and mucking up my commits.


## Todos

 - [x] commits implement semantic version and tag
 - [x] commit message is used for DB field AND git commit
 - [x] WIP 5-3-21 PH: need a way to see which fields have changed in the SQL-Alchemy event hooks
 - [x] 5-7-21 PH: Add event hook that listens for updates to field/commits/deletes (inserts work atm)
 - [x] 5-7-21 PH: Need to test event listener types
 - [x] 5-7-21 PH:need a linear get current tag in git and if exists, leverage it
 - [x] 5-10-21 PH: need a method to list an ordered dict or an ordered list of tags w commits
 - [ ] 5-13-2021 PH: need a way to roll back to previous commits
 - [ ] 5-13-2021 PH: a method that returns an easy overall status
 - [ ] 5-13-2021 PH: a method that returns all branches, commits, commit messages
 - [ ] 5-13-2021 PH: a merge request system
 - [ ] easy rollback to previous commit in both database and git
 - [ ] backscrub a git repo and update the database
 - [ ] 5-14-2021 PH: add support for taking a dictionary type, serializing it, then deserializing on retrieval

### 5-10-21 notes regarding tags API exposure

5-13-2021 PH: this is all set, minus the current branch part and is verbatim what you're seeing below.


 - [annotated tags are interesting here](https://git-scm.com/book/en/v2/Git-Basics-Tagging)
 - [checking out a specific tag](https://stackoverflow.com/questions/20073873/ - how-to-checkout-a-tag-with-gitpython)
 - [get tags paired up with the commits,](https://stackoverflow.com/questions/34932306/get-tags-of-a-commit) may have to pair this up & iterate back thru the commit hashes their paired off with to retrieve the commit msgs
 - [notice the remote origin push here as well](https://stackoverflow.com/questions/35845733/gitpython-create-and-push-tags)
 - [It looks like we can annotate the tags here](https://gitpython.readthedocs.io/en/stable/tutorial.html?highlight=create_tag)


datastructure should look something like this.

```
 { 'tag1.4': {
            'commit_hash': j,
            'branch': k,
            'current_branch': l, #ACTIVE BRANCH
            'current_commit': m, #ACTIVE COMMIT
            'commit_message': x,
            'author': y,
            'date': z
            }
  
 } 
```

A few other ideas:
 - use annotated tags (supports author, date, etc sort of metadata)

## Current/More recent commits

More recent commits will contain a shaped up version of the mixin as it comes closer to being a production usecase

## Earlier commits

This is some R&D I surfaced while working on making a git SQLAlchemy mixin. The concept being that the mixin would be plug & play and allow fields to be tracked individually in git.

~~The problems encountered as of 4/30/21 with this after both R&D and speaking with others in the SQLAlchemy community on Gitter/matrix protocol was that there is currently no prehook to both process the child objects (models) from within the mixin, then add new fields to the mixin or model with dynamic names.~~ I was able to successfully get this working (4/30/21).

The result is that moving forward I am going to purely be using single fields, then serializing the current record for that table.

IE:

instead of:

`{fieldname}_git_commit_message = Column(str...)`

```
git_commit_message = Column(str)
#git_commit_message = '{"fieldname" : "messageHere", "otherfieldname" : "otherMessageHere"}'
```



## Links

Exported from Chrome so some of this is cryptic, but more or less the links are present.
```

DL><p>
            <DT><A HREF="https://stackoverflow.com/questions/47371450/inherit-and-add-indexes-from-sqlalchemy-mixins" ADD_DATE="1619465116" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABXklEQVQ4jbWQsUsCYRjGn/fuSu/Sk3ALmlzNtoagKRqSaHMKGkKhEOV0KWispSXPQaglAnNobOgfaCyIcgicmxO9zFPv/N5WwTs5gt7x+5739/2eDwgw/bK67HcnBQG4Ag3L0LJ/BoBFDuDzTiGUCAywDC3bNbRtANCrwxaBziRZanAGcjADwR8AX1uGesEZyFGzXwO43VsKn07GaJa5lY/GMefUAYooEvaELDnCEW9M2I1V7GdPg04hlLAM7dYqqut67ftLNwdpMB5dgRfXdVMgHIFpx9egfbwYk0eDA2LKAWJMkK6cUOhOGdkpZmoQiy29OmwFq1AKb5CgQyakAXqQJKpELn/eJzPK1JKhPhHjk4EmMzUVmU/coVLkeXff672pk155YXUsxikCJQFeYVCSgCiAV920N311b+r37FslH413S+qaV86rggfIBbG38RRAN+2ZHzsTMKvGv80vvziHGAusG84AAAAASUVORK5CYII=">python - Inherit and add indexes from sqlalchemy mixins - Stack Overflow</A>
            <DT><A HREF="https://docs.sqlalchemy.org/en/14/orm/loading_columns.html#sqlalchemy.orm.deferred" ADD_DATE="1619465130" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAACXklEQVQ4jX2SS09aURSF9zmXl8jrQjA2bYzSiDwMopbSIFKjNbHtqFGH/g7/Qv+EQwc2cdDUpBOboNbgFQxeItJbrpYrVKQVikXk4eWcDmRgje2a7ax82dl7LbT4dhH+lkFnYE0sg5lSuXRRuaCU3nYVt4dObad/yO91e/Wdeoxx5bKSzWfT39IJISHL8l3A1mObeT7Tbe0WMyIX5wBBz4Mej8PjdXstZsv65/WbVW2gQ90xNTZlNpnXPq1F+SgFCgDbsD0kDk0HpyeeTVQuK1yco0AVAIAxDvlDVrN15cNKOpPue9TncXoo0KSQ5FN88Vdx4c1C0BeUvktnP88UAMAaWFe/K/k1mc6kB2wD86/nW3KLUOJxeFY/rqbEFP+FH3867rA5CucFDACskWUN7OmPU4TQyOAIUFh+v7z0bunq6mrYNYwRlnISpdSgNxBCFABAgTavm/VGXa1Sd1m6iuViLp8jlJQrZZ1Op1Qq5ZZMKcUIAwAGgFqtRgixstZ6ox7eCRv1xtmXs3Ov5nof9grHQqPZ0Ov0DGaq9Wr7S6WLUvl32dnv3Inv8Cleq9GG/CGM8FZsK7IXUSqVDpujed2UchIAMMEXQbklYwb7PD6VSnV0cnRyenKYPowfxg+EA0ppYCQQeBKIJWLcPte+AQCifFSr1k6OTWo0mt393cJ5QcEo7Db76OCo2+7OF/Kbu5s3YbcBQkiYCwOCoC/ofOys1qoIIZPBhBCK7EViiVipXLpbDUrpBrchZkSX3WUxWiilwpEgSqJwLLRarfvLRwjJ5rPZfBb+Lfwf7179Adr1I98msxgWAAAAAElFTkSuQmCC">Loading Columns — SQLAlchemy 1.4 Documentation</A>
            <DT><A HREF="https://docs.sqlalchemy.org/en/14/orm/events.html#instance-events" ADD_DATE="1619465535" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAACXklEQVQ4jX2SS09aURSF9zmXl8jrQjA2bYzSiDwMopbSIFKjNbHtqFGH/g7/Qv+EQwc2cdDUpBOboNbgFQxeItJbrpYrVKQVikXk4eWcDmRgje2a7ax82dl7LbT4dhH+lkFnYE0sg5lSuXRRuaCU3nYVt4dObad/yO91e/Wdeoxx5bKSzWfT39IJISHL8l3A1mObeT7Tbe0WMyIX5wBBz4Mej8PjdXstZsv65/WbVW2gQ90xNTZlNpnXPq1F+SgFCgDbsD0kDk0HpyeeTVQuK1yco0AVAIAxDvlDVrN15cNKOpPue9TncXoo0KSQ5FN88Vdx4c1C0BeUvktnP88UAMAaWFe/K/k1mc6kB2wD86/nW3KLUOJxeFY/rqbEFP+FH3867rA5CucFDACskWUN7OmPU4TQyOAIUFh+v7z0bunq6mrYNYwRlnISpdSgNxBCFABAgTavm/VGXa1Sd1m6iuViLp8jlJQrZZ1Op1Qq5ZZMKcUIAwAGgFqtRgixstZ6ox7eCRv1xtmXs3Ov5nof9grHQqPZ0Ov0DGaq9Wr7S6WLUvl32dnv3Inv8Cleq9GG/CGM8FZsK7IXUSqVDpujed2UchIAMMEXQbklYwb7PD6VSnV0cnRyenKYPowfxg+EA0ppYCQQeBKIJWLcPte+AQCifFSr1k6OTWo0mt393cJ5QcEo7Db76OCo2+7OF/Kbu5s3YbcBQkiYCwOCoC/ofOys1qoIIZPBhBCK7EViiVipXLpbDUrpBrchZkSX3WUxWiilwpEgSqJwLLRarfvLRwjJ5rPZfBb+Lfwf7179Adr1I98msxgWAAAAAElFTkSuQmCC">ORM Events — SQLAlchemy 1.4 Documentation</A>
            <DT><A HREF="https://docs.sqlalchemy.org/en/14/orm/events.html#sqlalchemy.orm.MapperEvents.before_configured" ADD_DATE="1619465583" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAACXklEQVQ4jX2SS09aURSF9zmXl8jrQjA2bYzSiDwMopbSIFKjNbHtqFGH/g7/Qv+EQwc2cdDUpBOboNbgFQxeItJbrpYrVKQVikXk4eWcDmRgje2a7ax82dl7LbT4dhH+lkFnYE0sg5lSuXRRuaCU3nYVt4dObad/yO91e/Wdeoxx5bKSzWfT39IJISHL8l3A1mObeT7Tbe0WMyIX5wBBz4Mej8PjdXstZsv65/WbVW2gQ90xNTZlNpnXPq1F+SgFCgDbsD0kDk0HpyeeTVQuK1yco0AVAIAxDvlDVrN15cNKOpPue9TncXoo0KSQ5FN88Vdx4c1C0BeUvktnP88UAMAaWFe/K/k1mc6kB2wD86/nW3KLUOJxeFY/rqbEFP+FH3867rA5CucFDACskWUN7OmPU4TQyOAIUFh+v7z0bunq6mrYNYwRlnISpdSgNxBCFABAgTavm/VGXa1Sd1m6iuViLp8jlJQrZZ1Op1Qq5ZZMKcUIAwAGgFqtRgixstZ6ox7eCRv1xtmXs3Ov5nof9grHQqPZ0Ov0DGaq9Wr7S6WLUvl32dnv3Inv8Cleq9GG/CGM8FZsK7IXUSqVDpujed2UchIAMMEXQbklYwb7PD6VSnV0cnRyenKYPowfxg+EA0ppYCQQeBKIJWLcPte+AQCifFSr1k6OTWo0mt393cJ5QcEo7Db76OCo2+7OF/Kbu5s3YbcBQkiYCwOCoC/ofOys1qoIIZPBhBCK7EViiVipXLpbDUrpBrchZkSX3WUxWiilwpEgSqJwLLRarfvLRwjJ5rPZfBb+Lfwf7179Adr1I98msxgWAAAAAElFTkSuQmCC">ORM Events — SQLAlchemy 1.4 Documentation</A>
            <DT><A HREF="https://docs.sqlalchemy.org/en/14/orm/events.html" ADD_DATE="1619465616" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAACXklEQVQ4jX2SS09aURSF9zmXl8jrQjA2bYzSiDwMopbSIFKjNbHtqFGH/g7/Qv+EQwc2cdDUpBOboNbgFQxeItJbrpYrVKQVikXk4eWcDmRgje2a7ax82dl7LbT4dhH+lkFnYE0sg5lSuXRRuaCU3nYVt4dObad/yO91e/Wdeoxx5bKSzWfT39IJISHL8l3A1mObeT7Tbe0WMyIX5wBBz4Mej8PjdXstZsv65/WbVW2gQ90xNTZlNpnXPq1F+SgFCgDbsD0kDk0HpyeeTVQuK1yco0AVAIAxDvlDVrN15cNKOpPue9TncXoo0KSQ5FN88Vdx4c1C0BeUvktnP88UAMAaWFe/K/k1mc6kB2wD86/nW3KLUOJxeFY/rqbEFP+FH3867rA5CucFDACskWUN7OmPU4TQyOAIUFh+v7z0bunq6mrYNYwRlnISpdSgNxBCFABAgTavm/VGXa1Sd1m6iuViLp8jlJQrZZ1Op1Qq5ZZMKcUIAwAGgFqtRgixstZ6ox7eCRv1xtmXs3Ov5nof9grHQqPZ0Ov0DGaq9Wr7S6WLUvl32dnv3Inv8Cleq9GG/CGM8FZsK7IXUSqVDpujed2UchIAMMEXQbklYwb7PD6VSnV0cnRyenKYPowfxg+EA0ppYCQQeBKIJWLcPte+AQCifFSr1k6OTWo0mt393cJ5QcEo7Db76OCo2+7OF/Kbu5s3YbcBQkiYCwOCoC/ofOys1qoIIZPBhBCK7EViiVipXLpbDUrpBrchZkSX3WUxWiilwpEgSqJwLLRarfvLRwjJ5rPZfBb+Lfwf7179Adr1I98msxgWAAAAAElFTkSuQmCC">ORM Events — SQLAlchemy 1.4 Documentation</A>
            <DT><A HREF="https://stackoverflow.com/questions/12753450/sqlalchemy-mixins-and-event-listener" ADD_DATE="1619465641" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABXklEQVQ4jbWQsUsCYRjGn/fuSu/Sk3ALmlzNtoagKRqSaHMKGkKhEOV0KWispSXPQaglAnNobOgfaCyIcgicmxO9zFPv/N5WwTs5gt7x+5739/2eDwgw/bK67HcnBQG4Ag3L0LJ/BoBFDuDzTiGUCAywDC3bNbRtANCrwxaBziRZanAGcjADwR8AX1uGesEZyFGzXwO43VsKn07GaJa5lY/GMefUAYooEvaELDnCEW9M2I1V7GdPg04hlLAM7dYqqut67ftLNwdpMB5dgRfXdVMgHIFpx9egfbwYk0eDA2LKAWJMkK6cUOhOGdkpZmoQiy29OmwFq1AKb5CgQyakAXqQJKpELn/eJzPK1JKhPhHjk4EmMzUVmU/coVLkeXff672pk155YXUsxikCJQFeYVCSgCiAV920N311b+r37FslH413S+qaV86rggfIBbG38RRAN+2ZHzsTMKvGv80vvziHGAusG84AAAAASUVORK5CYII=">python - Sqlalchemy mixins / and event listener - Stack Overflow</A>
            <DT><A HREF="https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/api.html#declare-last" ADD_DATE="1619465661" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAACXklEQVQ4jX2SS09aURSF9zmXl8jrQjA2bYzSiDwMopbSIFKjNbHtqFGH/g7/Qv+EQwc2cdDUpBOboNbgFQxeItJbrpYrVKQVikXk4eWcDmRgje2a7ax82dl7LbT4dhH+lkFnYE0sg5lSuXRRuaCU3nYVt4dObad/yO91e/Wdeoxx5bKSzWfT39IJISHL8l3A1mObeT7Tbe0WMyIX5wBBz4Mej8PjdXstZsv65/WbVW2gQ90xNTZlNpnXPq1F+SgFCgDbsD0kDk0HpyeeTVQuK1yco0AVAIAxDvlDVrN15cNKOpPue9TncXoo0KSQ5FN88Vdx4c1C0BeUvktnP88UAMAaWFe/K/k1mc6kB2wD86/nW3KLUOJxeFY/rqbEFP+FH3867rA5CucFDACskWUN7OmPU4TQyOAIUFh+v7z0bunq6mrYNYwRlnISpdSgNxBCFABAgTavm/VGXa1Sd1m6iuViLp8jlJQrZZ1Op1Qq5ZZMKcUIAwAGgFqtRgixstZ6ox7eCRv1xtmXs3Ov5nof9grHQqPZ0Ov0DGaq9Wr7S6WLUvl32dnv3Inv8Cleq9GG/CGM8FZsK7IXUSqVDpujed2UchIAMMEXQbklYwb7PD6VSnV0cnRyenKYPowfxg+EA0ppYCQQeBKIJWLcPte+AQCifFSr1k6OTWo0mt393cJ5QcEo7Db76OCo2+7OF/Kbu5s3YbcBQkiYCwOCoC/ofOys1qoIIZPBhBCK7EViiVipXLpbDUrpBrchZkSX3WUxWiilwpEgSqJwLLRarfvLRwjJ5rPZfBb+Lfwf7179Adr1I98msxgWAAAAAElFTkSuQmCC">declare last</A>
            <DT><A HREF="https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/api.html#declare-first" ADD_DATE="1619465678" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAACXklEQVQ4jX2SS09aURSF9zmXl8jrQjA2bYzSiDwMopbSIFKjNbHtqFGH/g7/Qv+EQwc2cdDUpBOboNbgFQxeItJbrpYrVKQVikXk4eWcDmRgje2a7ax82dl7LbT4dhH+lkFnYE0sg5lSuXRRuaCU3nYVt4dObad/yO91e/Wdeoxx5bKSzWfT39IJISHL8l3A1mObeT7Tbe0WMyIX5wBBz4Mej8PjdXstZsv65/WbVW2gQ90xNTZlNpnXPq1F+SgFCgDbsD0kDk0HpyeeTVQuK1yco0AVAIAxDvlDVrN15cNKOpPue9TncXoo0KSQ5FN88Vdx4c1C0BeUvktnP88UAMAaWFe/K/k1mc6kB2wD86/nW3KLUOJxeFY/rqbEFP+FH3867rA5CucFDACskWUN7OmPU4TQyOAIUFh+v7z0bunq6mrYNYwRlnISpdSgNxBCFABAgTavm/VGXa1Sd1m6iuViLp8jlJQrZZ1Op1Qq5ZZMKcUIAwAGgFqtRgixstZ6ox7eCRv1xtmXs3Ov5nof9grHQqPZ0Ov0DGaq9Wr7S6WLUvl32dnv3Inv8Cleq9GG/CGM8FZsK7IXUSqVDpujed2UchIAMMEXQbklYwb7PD6VSnV0cnRyenKYPowfxg+EA0ppYCQQeBKIJWLcPte+AQCifFSr1k6OTWo0mt393cJ5QcEo7Db76OCo2+7OF/Kbu5s3YbcBQkiYCwOCoC/ofOys1qoIIZPBhBCK7EViiVipXLpbDUrpBrchZkSX3WUxWiilwpEgSqJwLLRarfvLRwjJ5rPZfBb+Lfwf7179Adr1I98msxgWAAAAAElFTkSuQmCC">declare first</A>
            <DT><A HREF="https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/api.html#table-cls" ADD_DATE="1619465701" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAACXklEQVQ4jX2SS09aURSF9zmXl8jrQjA2bYzSiDwMopbSIFKjNbHtqFGH/g7/Qv+EQwc2cdDUpBOboNbgFQxeItJbrpYrVKQVikXk4eWcDmRgje2a7ax82dl7LbT4dhH+lkFnYE0sg5lSuXRRuaCU3nYVt4dObad/yO91e/Wdeoxx5bKSzWfT39IJISHL8l3A1mObeT7Tbe0WMyIX5wBBz4Mej8PjdXstZsv65/WbVW2gQ90xNTZlNpnXPq1F+SgFCgDbsD0kDk0HpyeeTVQuK1yco0AVAIAxDvlDVrN15cNKOpPue9TncXoo0KSQ5FN88Vdx4c1C0BeUvktnP88UAMAaWFe/K/k1mc6kB2wD86/nW3KLUOJxeFY/rqbEFP+FH3867rA5CucFDACskWUN7OmPU4TQyOAIUFh+v7z0bunq6mrYNYwRlnISpdSgNxBCFABAgTavm/VGXa1Sd1m6iuViLp8jlJQrZZ1Op1Qq5ZZMKcUIAwAGgFqtRgixstZ6ox7eCRv1xtmXs3Ov5nof9grHQqPZ0Ov0DGaq9Wr7S6WLUvl32dnv3Inv8Cleq9GG/CGM8FZsK7IXUSqVDpujed2UchIAMMEXQbklYwb7PD6VSnV0cnRyenKYPowfxg+EA0ppYCQQeBKIJWLcPte+AQCifFSr1k6OTWo0mt393cJ5QcEo7Db76OCo2+7OF/Kbu5s3YbcBQkiYCwOCoC/ofOys1qoIIZPBhBCK7EViiVipXLpbDUrpBrchZkSX3WUxWiilwpEgSqJwLLRarfvLRwjJ5rPZfBb+Lfwf7179Adr1I98msxgWAAAAAElFTkSuQmCC">table_cls</A>
            <DT><A HREF="https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Table" ADD_DATE="1619465746" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAACXklEQVQ4jX2SS09aURSF9zmXl8jrQjA2bYzSiDwMopbSIFKjNbHtqFGH/g7/Qv+EQwc2cdDUpBOboNbgFQxeItJbrpYrVKQVikXk4eWcDmRgje2a7ax82dl7LbT4dhH+lkFnYE0sg5lSuXRRuaCU3nYVt4dObad/yO91e/Wdeoxx5bKSzWfT39IJISHL8l3A1mObeT7Tbe0WMyIX5wBBz4Mej8PjdXstZsv65/WbVW2gQ90xNTZlNpnXPq1F+SgFCgDbsD0kDk0HpyeeTVQuK1yco0AVAIAxDvlDVrN15cNKOpPue9TncXoo0KSQ5FN88Vdx4c1C0BeUvktnP88UAMAaWFe/K/k1mc6kB2wD86/nW3KLUOJxeFY/rqbEFP+FH3867rA5CucFDACskWUN7OmPU4TQyOAIUFh+v7z0bunq6mrYNYwRlnISpdSgNxBCFABAgTavm/VGXa1Sd1m6iuViLp8jlJQrZZ1Op1Qq5ZZMKcUIAwAGgFqtRgixstZ6ox7eCRv1xtmXs3Ov5nof9grHQqPZ0Ov0DGaq9Wr7S6WLUvl32dnv3Inv8Cleq9GG/CGM8FZsK7IXUSqVDpujed2UchIAMMEXQbklYwb7PD6VSnV0cnRyenKYPowfxg+EA0ppYCQQeBKIJWLcPte+AQCifFSr1k6OTWo0mt393cJ5QcEo7Db76OCo2+7OF/Kbu5s3YbcBQkiYCwOCoC/ofOys1qoIIZPBhBCK7EViiVipXLpbDUrpBrchZkSX3WUxWiilwpEgSqJwLLRarfvLRwjJ5rPZfBb+Lfwf7179Adr1I98msxgWAAAAAElFTkSuQmCC">Table Object</A>
            <DT><A HREF="https://discourse.techart.online/t/python-fastest-way-to-recursively-list-files-of-specific-type/3081/5" ADD_DATE="1619465862" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAACgElEQVQ4jTXQz27cRBwH8O9vfjPjHdsbZ2PvJoE20JQ/EiAOFVUucAFFHMoVJCQEqEhceAAOPAQHxA3xDNxAiBO8QQSVWoVVUakIIQm7WY+9tce/4RDxCJ8PA9je3haRsiyBWBQb2hjnXJ45Y8ydW8N5rZPx7MbW+vbz6vgkKgCz2cw5V1WVS/OyLDeyYrKZd9iFnnxyZ9gtbN3dvLUf338jEDkGUBSF995a2/jaGLPu226dfHp4nMJ/+eOrVi0+f/f425+mP//+dAiXCkCMUUQAACQSiRARaq+6ANarPkrnFaugePC+UQDSNDXGOOeMNlmWUsxA4xd2ZbIpfZxtWN67IWxHWeYAMABmbppGRLxfNV3cyZZV7n/7w80f46Wd5Z9n68cn44cn6zAEX9cKwNZWaa3dnEzy3Fk7vf3K6q3Xlr+eXr+M5YdvXxRO37t4Js9G1VYFQANo23YIfds2fdcF3dTniupItOKhPXlEbRBt67qXpm0BKIAAxEgAAGbYgYQ4UtQQgwQMiBAQEQWABiFNnbFaeHKw/9dHb967+83NLmRffXD0y33+4ruDbHhw7bpZt9q5/9Fa67bxCYfFZXu65L/PJeHl0g/3H0Vg6DovAu9rEamv0LNpaUejC9l7+Ro+PnzSqmoZnnrv9f7gRdHpTpbYsirzPK+qCgAp4r1n95+sTj975/LrHzbWsnP43APr6PujfUMLl43Pzs6ns+ny30WxWcznc4UoRIoJZAiR+6gCs9UShiFAWCkipYhAUEpdtUYzGkmryjJq5hHrLI9pQsbYRBubWGZYa5nZGAOAI8BE66Yd03D0UHyHbKgvFnH+jwp92/eD9x6I3vsr9H8CYit4HgVzEQAAAABJRU5ErkJggg==">virtualize git repo into blob and into field</A>
            <DT><A HREF="https://www.michaelcho.me/article/sqlalchemy-commit-flush-expire-refresh-merge-whats-the-difference" ADD_DATE="1619543222" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACEElEQVQ4jY2Tz0tUURzFP9973ziPmdBCi7FGKMxSahstNapVSC5KCKQgK9okGbQIWrQIgjZFBKIFBu0SN0K0aXAd+AeUKKLZLyPS5onOm/fut4XOpM5bdFb3wvece87he4Ut6How6dXnm086pQ/oQtmPoKr6RYRJ5+zr7J62qbFeiSscqRx6Rud2l8vrgyJyA8iRjK8oQ3HGPnvX1/anKnBmeLbBN+UnwBXAON2YNpvyO+6xKi+t5e5Ef3vRoCq+lG8BlwFjRTiyN82xnE+dFdKecDzn09aUrghYEfqd4yaAdI98OqGi40CLAtmU4f7ZZvINdTx8/42UEe6dzjH7q8SjwnfWI1eJM2egx3Nor0BLNaWAZ4QG33K4KU3KCvW+JWWqdVVw0MEFT4TOpLaCMKZjn49nhKDk0NoREbTTAw4kCXxeDmltTKPA4kqI1BgARfIGasWNwFIQoUDklJ9BRAIfATXAQpKD4nrMUhDxoxixGsZIggWFeYNQ2OnCGqHslMXlkMWVkMiBreU7RQuei/WNNXJJoVU2LX+YX2VhOSQoxcQKjRnL77WIWLe9M22NjAvAuRcfbxt4rJBKipOAksLg2+vtQwbAuGDEqT4Hwv8hi/A0U8y+gi2fqXt4KoPZdQ0YUDgEmJ2ZgRllgzx2p2VtmwAAqnJ+dKYjjt1F0FP829AFlIKxjE1cPTqNSLWMv+8ly1a9RZPlAAAAAElFTkSuQmCC">Michael Cho :: SQLAlchemy commit(), flush(), expire(), refresh(), merge() - what&#39;s the difference? - Python</A>
            <DT><A HREF="https://xnuinside.medium.com/sqlalchemy-metaclasses-and-declarative-base-configure-db-models-classes-a904429d728a" ADD_DATE="1619718924" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABlElEQVQ4jaWTsaoiQRBFT3e/mUFBmET8BH/ABQN/wFARFBTBSJjAVDQQzIwe7IcYjGBgZiCYGhr4ASZmBsLYrzZQm9G3y8puQdNwq2717erbAJ9AAljgC5C/rK977RX4VHeQ+654L1ytTnVWxphHM4wxTwxjzAN7kAUQdZek+DcFolMk1e/3ieOY5XLJcDgkm806RrPZZDAYAOD7vrrnFEopCYJA5vO5vMZ2u5VMJiOlUslhrVZLOp2OjMdjAeRDRGg0GtTrdZIkQamboOv1SrlcJooi8vk8IoK1lna7zfF4JAxDAD4AqtUq1lo3LKUUSimstdRqNc7ns8sVi8WnIWsAz/PcyelQSmGMQWv9hIm4x7o1WK1WaK2dTGstSZKgtWaxWLDb7VzucDhwOp24XC6uo/i+L3Ecfxvifr+XMAylUqk4rNvtSq/Xk8lk8vDPzRBBEMhoNJL1ei2bzUZms5kUCgVn4SiKZDqdiud5EgSB5HK594z0euffGckBr1ZOk/9gZf7XyhggBH6kVb9BFm5f+ucvMhDxQnv5W1IAAAAASUVORK5CYII=">SQLAlchemy, metaclasses and declarative_base: configure DB model’s classes | by Iuliia Volkova | Medium</A>
            <DT><A HREF="https://mgarod.medium.com/dynamically-add-a-method-to-a-class-in-python-c49204b85bd6" ADD_DATE="1619729318" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABlElEQVQ4jaWTsaoiQRBFT3e/mUFBmET8BH/ABQN/wFARFBTBSJjAVDQQzIwe7IcYjGBgZiCYGhr4ASZmBsLYrzZQm9G3y8puQdNwq2717erbAJ9AAljgC5C/rK977RX4VHeQ+654L1ytTnVWxphHM4wxTwxjzAN7kAUQdZek+DcFolMk1e/3ieOY5XLJcDgkm806RrPZZDAYAOD7vrrnFEopCYJA5vO5vMZ2u5VMJiOlUslhrVZLOp2OjMdjAeRDRGg0GtTrdZIkQamboOv1SrlcJooi8vk8IoK1lna7zfF4JAxDAD4AqtUq1lo3LKUUSimstdRqNc7ns8sVi8WnIWsAz/PcyelQSmGMQWv9hIm4x7o1WK1WaK2dTGstSZKgtWaxWLDb7VzucDhwOp24XC6uo/i+L3Ecfxvifr+XMAylUqk4rNvtSq/Xk8lk8vDPzRBBEMhoNJL1ei2bzUZms5kUCgVn4SiKZDqdiud5EgSB5HK594z0euffGckBr1ZOk/9gZf7XyhggBH6kVb9BFm5f+ucvMhDxQnv5W1IAAAAASUVORK5CYII=">Dynamically Add a Method to a Class in Python | by Michael Garod | Medium</A>
            <DT><A HREF="https://stackoverflow.com/questions/55925297/how-to-use-my-own-meta-class-together-with-sqlalchemy-model-as-a-parent-class" ADD_DATE="1619729325" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABXklEQVQ4jbWQsUsCYRjGn/fuSu/Sk3ALmlzNtoagKRqSaHMKGkKhEOV0KWispSXPQaglAnNobOgfaCyIcgicmxO9zFPv/N5WwTs5gt7x+5739/2eDwgw/bK67HcnBQG4Ag3L0LJ/BoBFDuDzTiGUCAywDC3bNbRtANCrwxaBziRZanAGcjADwR8AX1uGesEZyFGzXwO43VsKn07GaJa5lY/GMefUAYooEvaELDnCEW9M2I1V7GdPg04hlLAM7dYqqut67ftLNwdpMB5dgRfXdVMgHIFpx9egfbwYk0eDA2LKAWJMkK6cUOhOGdkpZmoQiy29OmwFq1AKb5CgQyakAXqQJKpELn/eJzPK1JKhPhHjk4EmMzUVmU/coVLkeXff672pk155YXUsxikCJQFeYVCSgCiAV920N311b+r37FslH413S+qaV86rggfIBbG38RRAN+2ZHzsTMKvGv80vvziHGAusG84AAAAASUVORK5CYII=">python - How to use my own Meta class together with SQLAlchemy-Model as a parent class - Stack Overflow</A>
        </DL><p>

```