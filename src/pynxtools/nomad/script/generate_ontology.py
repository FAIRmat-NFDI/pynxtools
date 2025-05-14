import owlready2
from .NeXusOntology import NeXusOntology
import pygit2
import os
import sys

def main(full=False):
  print(f"Debug: Generating ontology with full={full}")
  local_dir = os.path.abspath(os.path.dirname(__file__))
  nexus_def_path = os.path.join(local_dir, f"..{os.sep}..{os.sep}definitions")
  os.environ['NEXUS_DEF_PATH']=nexus_def_path

  repo = pygit2.Repository(nexus_def_path)
  # Check for provided commit hash argument
  # if len(sys.argv) > 2:
  #     commit_hash = sys.argv[2]
  #     try:
  #         # Use the provided commit hash directly
  #         commit = repo.revparse_single(commit_hash)
  #         repo.checkout_tree(commit)
  #         repo.set_head(commit.id)  # Update HEAD to point to the commit
  #         def_commit = commit_hash[:7]  # Use the provided commit hash
  #         print(f"Checked out commit hash: {commit_hash} (commit: {def_commit})")
  #     except KeyError:
  #         print(f"Error: Commit hash '{commit_hash}' not found in the repository.")
  #         sys.exit(1)
  # else:
  #     # Use the current HEAD commit if no version is specified
  def_commit = str(repo.head.target)[:7]

  # Official NeXus definitions: https://manual.nexusformat.org/classes/
  web_page_base_prefix = 'https://manual.nexusformat.org/'

  detailed_iri = 'http://purl.org/nexusformat/v2.0/definitions/' + def_commit + '/'
  base_iri = 'http://purl.org/nexusformat/definitions/'
  onto = owlready2.get_ontology(base_iri + "NeXusOntology")

  nexus_ontology = NeXusOntology(onto, base_iri, web_page_base_prefix, def_commit, full)
  nexus_ontology.gen_classes()
  nexus_ontology.gen_children()
  if full:
    print("Debug: Generating full ontology datasets...")
    nexus_ontology.gen_datasets()
    fullsuffix='_full'
  else:
    fullsuffix=''
  output_path = os.path.join(local_dir, f"..{os.sep}ontology{os.sep}NeXusOntology{fullsuffix}.owl")
  print(f"Debug: Saving ontology to {output_path}")
  onto.save(file=output_path, format="rdfxml")

if __name__ == "__main__":
    import sys
    full = len(sys.argv) > 1 and sys.argv[1] == 'full'
    main(full=full)