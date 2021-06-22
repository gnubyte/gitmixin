# Using the GitMixin Library

This is an elaboration on how to use the library once it has been added to your project. See the getting started section for how to add GitMixin to your project.

Under getting started make sure you meet the requirements to use this library.

## Return all tags(Versions) and Commits

Each record in a table can return a tagmap if it is being tracked using GitMixin. This can be achieved by passing the model the name of the field you wish to retrieve the tagmap for, as well as the record ID.

```
currentProduct = Product.query.filter_by(id=101).first()
allVersionsOfProductDescription = currentProduct.return_all_tags_and_commits('productDescription', 202)
```