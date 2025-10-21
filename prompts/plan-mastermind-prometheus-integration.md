ok help me plan this out. big brain power needed here!

our main data engineering stack is in another repo. it's called prometheus. And in that repository, we use dbt and Dagster. We're using a hybrid approach with a Kubernetes cluster to host a containerized version of the repository that Dagster Cloud can then use to materialize assets.

What I need to do now is figure out how to get the dbt models that are here in Mastermind loaded with our other assets. I also need to figure out how to enable Prometheus to use the Python logic in Mastermind to call services. So Prometheus should be able to say, "Okay, we need to calculate new primary affiliations, we need to calculate new specialties, whatever it is." And so it needs to be able to call those specific services from Mastermind.

Can you walk me through a few different options of how we can do this?

Focus on strategies that would be easy to implement at the beginning but scalable.
